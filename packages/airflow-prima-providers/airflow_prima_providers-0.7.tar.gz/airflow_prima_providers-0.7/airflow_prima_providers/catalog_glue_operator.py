from airflow.models import BaseOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.decorators import apply_defaults

from airflow.providers.prima.glue_custom_crawler.descriptors import GlueTableDescriptor
from airflow.providers.prima.glue_custom_crawler.managers import GlueDataCatalogManager


class GlueCatalogCreateTableOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 database,
                 table,
                 table_type,
                 s3_bucket_table_input=None,
                 s3_key_table_input=None,
                 text_table_input=None,
                 *args, **kwargs):

        super(GlueCatalogCreateTableOperator, self).__init__(*args, **kwargs)
        self.database = database
        self.table = table
        self.table_type = table_type
        self.s3_bucket_table_input = s3_bucket_table_input
        self.s3_key_table_input = s3_key_table_input
        self.text_table_input = text_table_input

    def execute(self, context):
        data_catalog_manager = GlueDataCatalogManager()
        s3hook = S3Hook()

        # retrive table definition from text
        if self.text_table_input is not None:
            self.log.info("Read from text from resource {0}".format(self.text_table_input))
            text_table_input: str = self.text_table_input
            table_input_dict = dict(text_table_input)
            self.log.info("Read from text {0}".format(table_input_dict))
        elif self.s3_bucket_table_input is not None and self.s3_key_table_input is not None:
            # retrieve table definition from s3
            self.log.info("Read S3 file from {0}/{1}".format(self.s3_bucket_table_input, self.s3_key_table_input))
            table_input_from_s3: str = s3hook.read_key(self.s3_key_table_input, self.s3_bucket_table_input)
            table_input_dict = eval(table_input_from_s3)
        else:
            table_input_dict = None

        table_input: GlueTableDescriptor = GlueTableDescriptor.get_table_descriptor_with_db(self.database, table_input_dict[self.table_type])

        table_desc = data_catalog_manager.dc_search_table(self.database, self.table)
        if table_desc:
            self.log.info(f"Table {self.database}.{self.table} found: {table_desc}")
            if table_desc != table_input:
                self.log.info(f"Updating table {self.database}.{self.table} with request {table_input}")
                response = data_catalog_manager.update_dc_table(table_input)
                self.log.info("response {0}".format(response))
            else:
                self.log.info(f"Table {self.database}.{self.table} is up to date")
        else:
            self.log.info(f"Creating table {self.database}.{self.table} with request {table_input}")
            response = data_catalog_manager.create_dc_table(table_input)
            self.log.info("response {0}".format(response))
