import logging, logging.config

from airflow.providers.prima.glue_custom_crawler.managers import GlueDataCatalogManager, GluePostgresMetadataManager


class GluePostgresCustomCrawler:

    def __init__(self,
                 glue_database: str,
                 glue_connection_name: str,
                 crawling_pattern: str):
        self.glue_database = glue_database
        self.glue_connection_name = glue_connection_name
        self.crawling_pattern = crawling_pattern

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def start_crawl(self):
        self.logger.info("starting crawler with following parameters")
        self.logger.info(" - postgres connection: {}".format(self.glue_connection_name))
        self.logger.info(" - Glue output database: {}".format(self.glue_database))
        self.logger.info(" - Glue crawling pattern: {}".format(self.crawling_pattern))

        self.logger.info("connecting to Glue Data Catalog")
        self.logger.info("retrieving connection info for {}".format(self.glue_connection_name))
        connection_desc = GlueDataCatalogManager().get_connection(self.glue_connection_name)
        self.logger.info("connecting to Postgres using connection info")
        db_connection = GluePostgresMetadataManager.get_postgres_metadata_manager(connection_desc)

        self.logger.info("searching tables that match '{}' crawling pattern".format(self.crawling_pattern))
        table_list = db_connection.get_tables_for_pattern(self.crawling_pattern)

        if len(table_list) > 0:
            self.logger.info("the following tables will be crawled: {}".format(table_list))
            for table in table_list:
                self.logger.info("crawling table {}".format(table))
                self.crawl_table(table[0], table[1], db_connection)
        else:
            self.logger.warning("table search has returned 0 results for given pattern")

    def crawl_table(self, schema, table, db_connection):
        current_table_metadata = db_connection.get_metadata_from_postgres(self.glue_database, schema, table)
        table_response = GlueDataCatalogManager().dc_search_table(self.glue_database, current_table_metadata.name)

        if current_table_metadata == table_response:
            self.logger.info('table {} in the data catalog under {} is up to date'.format(
                current_table_metadata.name,
                self.glue_database
            ))
        elif table_response:
            self.logger.info('postgres table {}.{} has changed: updating data catalog'.format(db_connection.database, table))
            GlueDataCatalogManager().update_dc_table(current_table_metadata)
        else:
            self.logger.info('table {} not present in the data catalog under {}: creating it'.format(
                current_table_metadata.name,
                self.glue_database
            ))
            GlueDataCatalogManager().create_dc_table(current_table_metadata)
