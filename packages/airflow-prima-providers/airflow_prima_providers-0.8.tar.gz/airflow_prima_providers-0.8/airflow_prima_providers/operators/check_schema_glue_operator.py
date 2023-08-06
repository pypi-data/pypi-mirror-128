from airflow.providers.amazon.aws.hooks.glue_catalog import AwsGlueCatalogHook

from airflow import AirflowException
from airflow.models import BaseOperator

from airflow.utils.decorators import apply_defaults

import json

from dynamodb_operator import AwsDynamoDBHookCustom


class CheckSchemaGlueCatalogOperator(BaseOperator):
    ui_color = '#358145'

    @apply_defaults
    def __init__(self,
                 database,
                 table,
                 dynamo_table,
                 *args, **kwargs):

        super(CheckSchemaGlueCatalogOperator, self).__init__(*args, **kwargs)
        self.database = database
        self.table = table
        self.dynamo_table = dynamo_table

    def execute(self, context):
        glue_catalog_hook = AwsGlueCatalogHook()
        self.log.info("Check if table exits")
        table_glue: dict = glue_catalog_hook.get_table(database_name=self.database, table_name=self.table)
        table_schema_glue = table_glue['StorageDescriptor']['Columns']
        if table_glue is not None and table_glue['Name'] == self.table:
            self.log.info(f"The table {self.table} exists into DB {self.database}")
        else:
            self.log.info(f"The table {self.table} not exists into DB {self.database}")
            raise AirflowException(f"The table {self.table} not exists into DB {self.database}")

        dynamo_hook = AwsDynamoDBHookCustom(table_keys=list("key"), table_name=self.dynamo_table)

        try:
            key = f"{self.database}_{self.table}"
            self.log.info("Get scheme table present in Dynamo with key  {0} ".format(key))
            table_schema_dynamo = dynamo_hook.get_item(key={"key": key})
            self.log.info("The scheme table present in Dynamo is {0} ".format(table_schema_dynamo))
            if 'Item' not in table_schema_dynamo:
                self.log.warning(f'The scheme table for {key} is not present in DynamoDB: creating it ')
                dynamo_hook.put_item(item={
                    "key": key,
                    "schema": table_schema_glue
                })
                table_schema_dynamo = dynamo_hook.get_item(key={"key": key})
        except Exception as general_error:
            raise AirflowException(f"Failed to insert items in dynamodb, error: {str(general_error)}")
        self.log.info(f"The schema glue {table_schema_glue}")
        self.log.info(f"The schema dynamo {table_schema_dynamo['Item']['schema']}")
        if table_schema_dynamo['Item']['schema'] != table_schema_glue:
            raise AirflowException(f"Schema of table {self.database}_{self.table} is changed")
