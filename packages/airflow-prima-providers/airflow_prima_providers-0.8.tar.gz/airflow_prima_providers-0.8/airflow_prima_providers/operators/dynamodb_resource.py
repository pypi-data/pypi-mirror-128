import logging

from boto3.dynamodb.table import TableResource

logger = logging.getLogger(__name__)


def register_table_methods(base_classes, **kwargs):
    base_classes.insert(0, DynamoTableResource)


class DynamoTableResource(TableResource):

    def __init__(self, table_name, client):
        """

        :type table_name: str
        :param table_name: The name of the table.  The class handles
            batch writes to a single table.

        :type client: ``botocore.client.Client``
        :param client: A botocore client.  Note this client
            **must** have the dynamodb customizations applied
            to it for transforming AttributeValues into the
            wire protocol.  What this means in practice is that
            you need to use a client that comes from a DynamoDB
            resource if you're going to instantiate this class
            directly, i.e
            ``boto3.resource('dynamodb').Table('foo').meta.client``.

        """
        self._table_name = table_name
        self._client = client

    def get_item(self, key):
        # try:
        response = self.meta.client.get_item(key=key)
        # except ClientError as e:
        #     print(e.response['Error']['Message'])
        # else:
        return response['Item']
