import logging, logging.config

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.prima.glue_custom_crawler.glue_crawler import GluePostgresCustomCrawler


class GlueCustomCrawlerOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 glue_database,
                 glue_connection_name,
                 crawling_pattern,
                 *args, **kwargs):

        super(GlueCustomCrawlerOperator, self).__init__(*args, **kwargs)
        self.glue_database = glue_database
        self.glue_connection_name = glue_connection_name
        self.crawling_pattern = crawling_pattern

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def execute(self, context):
        custom_crawler = GluePostgresCustomCrawler(
            glue_database=self.glue_database,
            glue_connection_name=self.glue_connection_name,
            crawling_pattern=self.crawling_pattern
        )

        custom_crawler.start_crawl()
