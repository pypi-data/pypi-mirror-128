from cached_property import cached_property

from airflow.models import BaseOperator
from airflow.providers.amazon.aws.hooks.glue_crawler import AwsGlueCrawlerHook
from airflow.utils.decorators import apply_defaults


class AwsGlueCrawlerTriggerOperator(BaseOperator):
    """
    Creates, updates and triggers an AWS Glue Crawler. AWS Glue Crawler is a serverless
    service that manages a catalog of metadata tables that contain the inferred
    schema, format and data types of data stores within the AWS cloud.

    :param config: Configurations for the AWS Glue crawler
    :type crawler_name: Name of crawler
    :param aws_conn_id: aws connection to use
    :type aws_conn_id: Optional[str]
    :param poll_interval: Time (in seconds) to wait between two consecutive calls to check crawler status
    :type poll_interval: Optional[int]
    """

    ui_color = '#ededed'

    @apply_defaults
    def __init__(
            self,
            crawler_name,
            aws_conn_id='aws_default',
            poll_interval: int = 5,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.aws_conn_id = aws_conn_id
        self.poll_interval = poll_interval
        self.crawler_name = crawler_name

    @cached_property
    def hook(self) -> AwsGlueCrawlerHook:
        """Create and return an AwsGlueCrawlerHook."""
        return AwsGlueCrawlerHook(self.aws_conn_id)

    def execute(self, context):
        """
        Executes AWS Glue Crawler from Airflow

        :return: the name of the current glue crawler.
        """
        self.log("Trigger crawler  {0}".format(self.crawler_name))

        self.log.info("Triggering AWS Glue Crawler")
        self.hook.start_crawler(self.crawler_name)
        self.log.info("Waiting for AWS Glue Crawler")
        self.hook.wait_for_crawler_completion(crawler_name=self.crawler_name, poll_interval=self.poll_interval)

        return self.crawler_name
