# from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
# from boto3.dynamodb.table import TableResource
# from botocore.exceptions import ClientError

import logging

"""This module contains the AWS DynamoDB hook"""
from typing import List, Optional

from airflow.exceptions import AirflowException
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook


class AwsDynamoDBHookCustom(AwsBaseHook):
    """
    Interact with AWS DynamoDB.

    Additional arguments (such as ``aws_conn_id``) may be specified and
    are passed down to the underlying AwsBaseHook.

    .. seealso::
        :class:`~airflow.providers.amazon.aws.hooks.base_aws.AwsBaseHook`

    :param table_keys: partition key and sort key
    :type table_keys: list
    :param table_name: target DynamoDB table
    :type table_name: str
    """

    def __init__(
            self, *args, table_keys: Optional[List] = None, table_name: Optional[str] = None, **kwargs
    ) -> None:
        self.table_keys = table_keys
        self.table_name = table_name
        kwargs["resource_type"] = "dynamodb"
        super().__init__(*args, **kwargs)

    def get_item(self, key: dict) -> dict:
        """Write batch items to DynamoDB table with provisioned throughout capacity."""
        try:
            table = self.get_conn().Table(self.table_name)
            logging.info("Table {0}".format(table))
            return table.get_item(Key=key)
        except Exception as general_error:
            raise AirflowException(f"Failed to get item in dynamodb, error: {str(general_error)}")

    def put_item(self, item: dict):
        """Write batch items to DynamoDB table with provisioned throughout capacity."""
        try:
            table = self.get_conn().Table(self.table_name)
            logging.info("Table {0}".format(table))
            table.put_item(Item=item)
        except Exception as general_error:
            raise AirflowException(f"Failed to put item in dynamodb, error: {str(general_error)}")
