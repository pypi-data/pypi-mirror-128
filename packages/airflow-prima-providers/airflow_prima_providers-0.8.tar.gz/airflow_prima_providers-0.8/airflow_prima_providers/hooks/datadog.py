
from typing import Any, Dict, List, Optional, Union

from datadog import api, initialize

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin


class DatadogHook(BaseHook, LoggingMixin):
    """
    Uses datadog API to send metrics of practically anything measurable,
    so it's possible to track # of db records inserted/deleted, records read
    from file and many other useful metrics.

    Depends on the datadog API, which has to be deployed on the same server where
    Airflow runs.

    :param datadog_conn_id: The connection to datadog, containing metadata for api keys.
    :param datadog_conn_id: str
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 app_key: Optional[str] = None,
                 datadog_conn_id: str = 'datadog_default'
                 ) -> None:
        super().__init__()
        if api_key:
            self.api_key = api_key
            self.app_key = app_key
        else:
            conn = self.get_connection(datadog_conn_id)
            self.api_key = conn.extra_dejson.get('api_key', None)
            self.app_key = conn.extra_dejson.get('app_key', None)

        if self.api_key is None:
            raise AirflowException("api_key must be specified in the Datadog connection details")

        self.log.info("Setting up api keys for Datadog")
        initialize(api_key=self.api_key, app_key=self.app_key)

    def validate_response(self, response: Dict[str, Any]) -> None:
        """Validate Datadog response"""
        if response['status'] != 'ok':
            self.log.error("Datadog returned: %s", response)
            raise AirflowException("Error status received from Datadog")

    def send_metric(
            self,
            metric_name: str,
            datapoint: Union[float, int],
            tags: Optional[List[str]] = None,
            type_: Optional[str] = None,
            interval: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Sends a single datapoint metric to DataDog

        :param metric_name: The name of the metric
        :type metric_name: str
        :param datapoint: A single integer or float related to the metric
        :type datapoint: int or float
        :param tags: A list of tags associated with the metric
        :type tags: list
        :param type_: Type of your metric: gauge, rate, or count
        :type type_: str
        :param interval: If the type of the metric is rate or count, define the corresponding interval
        :type interval: int
        """
        response = api.Metric.send(
            metric=metric_name, points=datapoint, tags=tags, type=type_, interval=interval
        )

        self.validate_response(response)
        return response
