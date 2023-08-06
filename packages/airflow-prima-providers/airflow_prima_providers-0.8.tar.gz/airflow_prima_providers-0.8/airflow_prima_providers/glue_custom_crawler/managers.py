import boto3
import re

from typing import List
from psycopg2 import connect

from glue_custom_crawler.descriptors import GlueTableDescriptor, StorageDescriptor, ColumnDescriptor, \
    ConnectionDescriptor


class GlueDataCatalogManager:
    """
    main class to interact with the Glue Data Catalog, allows to:

    - create a table
    - update an existing table
    - get a specific table
    - search a specific table
    - return a connection in the Data Catalog
    """

    def __init__(self):
        self.client = boto3.client('glue')

    def create_dc_table(self, table_descriptor: GlueTableDescriptor):
        return self.client.create_table(
            DatabaseName=table_descriptor.database_name,
            TableInput=table_descriptor.to_glue_full_descriptor()
        )

    def update_dc_table(self, table_descriptor: GlueTableDescriptor):
        return self.client.update_table(
            DatabaseName=table_descriptor.database_name,
            TableInput=table_descriptor.to_glue_full_descriptor()
        )

    def get_dc_table(self, database, table):
        return self.client.get_table(
            DatabaseName=database,
            Name=table
        )

    def dc_search_table(self, database_name, table_name):
        response = self.client.search_tables(SearchText=table_name)

        table_list = list(
            filter(lambda table_desc: table_desc.database_name == database_name and table_desc.name == table_name,
                   map(lambda table_resp: GlueTableDescriptor.get_table_descriptor(table_resp), response['TableList']))
        )

        return table_list[0] if table_list else None

    def get_connection(self, connection_name):
        glue_conn_desc = self.client.get_connection(
            Name=connection_name
        )

        return ConnectionDescriptor.get_connection_descriptor(glue_conn_desc)


class GluePostgresMetadataManager:
    """
    GluePostgresMetadataManager allows to interact with a Postgres DB
    to retrieve the metadata in a form that allows an immediate interaction
    with the Glue Data Catalog. The main functionalities are:

    - retrieve the tables into a database that match a pattern in the form of
      <schema_name>/(<table_name>|<table_prefix>%)
    - return the metatada information for a table in the postgres DB enriched
      with the information of the associated database and table in the Data
      Catalog
    - map the postgres data types to the spark data types
    """

    url_regex = '^[^/]+//([^/:]+):(\d+)/(\w+)$'
    crawling_pattern_regex = '^([^/]+)/([^/]+)$'

    data_type_map = {
        'varchar': 'string',
        'numeric': 'decimal',
        'int4': 'integer',
        'bool': 'boolean',
        'int8': 'long',
        'float8': 'double',
        'float4': 'float',
        'date': 'date',
        'time': 'timestamp',
        'timestamp': 'timestamp',
        'uuid': 'string',
        'text': 'string',
        'money': 'double',
        'bit': 'binary',
        'bpchar': 'string',
        'varbit': 'string'
    }

    def __init__(self,
                 url: str,
                 username: str,
                 password: str):
        url_match = re.search(self.url_regex, url)
        self.host = url_match.group(1)
        self.port = url_match.group(2)
        self.database = url_match.group(3)
        self.connection = connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=username,
            password=password
        )

    @staticmethod
    def get_postgres_metadata_manager(connection_descr: ConnectionDescriptor):
        return GluePostgresMetadataManager(
            url=connection_descr.url,
            username=connection_descr.username,
            password=connection_descr.password
        )

    def get_metadata_from_postgres(self, glue_database, source_schema, source_table):

        columns_list = self.__get_table_columns(source_schema, source_table)
        mapped_columns_list = self.__map_columns_to_dc_types(columns_list)

        if mapped_columns_list:
            sorted_columns = sorted(mapped_columns_list, key=lambda row: row[0])
            columns_desc = list(map(lambda row: {'Name': row[1], 'Type': row[2], 'Comment': None}, sorted_columns))

            return GlueTableDescriptor(
                database_name=glue_database,
                name='{}_{}_{}'.format(self.database, source_schema, source_table),
                storage_descriptor=StorageDescriptor(
                    location='{}.{}.{}'.format(self.database, source_schema, source_table),
                    columns=[ColumnDescriptor.get_column_descriptor(col) for col in columns_desc],
                    compressed=False,
                    stored_as_subdirectories=False
                ),
                partition_keys=None,
                table_type=None
            )
        else:
            return None

    def __get_table_columns(self, schema_name, table_name):
        query = """
            select ordinal_position,
                   column_name,
                   udt_name,
                   character_maximum_length,
                   numeric_precision,
                   numeric_scale
              from information_schema.columns
             where table_name = '{}'
               and table_schema = '{}';
        """.format(table_name, schema_name)

        with self.connection.cursor() as cur:
            cur.execute(query)
            columns_list = cur.fetchall()

        return columns_list if columns_list else None

    def __map_columns_to_dc_types(self, columns_list):
        """
        takes the response from the Postgres Query and
        maps the data types to the spark one.

        NB the logic to map the types is implemented based on
        the mapping done by spark reading the postgres table
        :param columns_list:
        :return:
        """

        def map_data_type(column):
            if column[2] in self.data_type_map:
                column[2] = self.data_type_map[column[2]]
            else:
                column[2] = 'string'
            return column

        def refine_column(column: List[str]):
            if column[2] == 'decimal':
                precision = column[4] if column[4] else '38'
                scale = column[5] if column[5] else '0'
                column[2] = f'{column[2]}({precision},{scale})'
            elif column[2] == 'binary' and int(column[3]) == 1:
                column[2] = 'boolean'

            return column

        prepared_columns = map(lambda col: list(col), columns_list)
        mapped_columns = map(map_data_type, prepared_columns)
        refined_columns = map(refine_column, mapped_columns)

        return list(refined_columns)

    def get_tables_for_pattern(self, crawling_pattern):
        crawling_pattern_match = re.search(self.crawling_pattern_regex, crawling_pattern)

        postgres_schema = crawling_pattern_match.group(1)
        postgres_table_pattern = crawling_pattern_match.group(2)

        query = """
            select table_schema, table_name
              from information_schema.tables
             where table_schema = '{}'
               and table_name like '{}';
        """.format(postgres_schema, postgres_table_pattern)

        with self.connection.cursor() as cur:
            cur.execute(query)
            columns_list = cur.fetchall()

        return columns_list if columns_list else None
