
from typing import Any, Dict, Optional, Union, List

from airflow.models import BaseOperator

from airflow.providers.prima.hooks.datadog import DatadogHook


class DataDogOperator(BaseOperator):
    """
    This operator allows you to send metrics of practically anything measurable,
    so it's possible to track # of db records inserted/deleted, records read
    from file and many other useful metrics.

    iIt api_key and app_key params is not supplied, datadog_conn_id will be used
    to save api_keu and app_key in the extra json section like this:

            {
             "app_key": "123456asdfg",\n
             "api_key": "123456asdfg"
            }

    Depends on the datadog API, which has to be deployed on the same server where
    Airflow runs.

    :param datadog_conn_id: The connection to datadog, containing metadata for api keys.
    :param datadog_conn_id: str
    :param api_key: Slack api key to connect to datadog
    :type api_key: Optional[str]
    :param app_key: The message you want to send on Slack
    :type app_key: Optional[str]
    :param metric_name: The name of the metric
    :type metric_name: str
    :param datapoint: A single integer or float related to the metric
    :type datapoint: int or float
    :param tags: A list of tags associated with the metric
    :type tags: list
    :param type_: Type of your metric: gauge, rate, or count
    :type type_: str
    :param interval: If the type of the metric is rate or count, define the corresponding interval
    :type interval: inte message should be posted to
    :type tags: List[str]
    """

    template_fields = [
        'datadog_conn_id',
        'name_metric',
        'datapoint',
        'tags',
        'interval',
        'type_'
    ]

    def __init__(
            self,
            *,
            name_metric: str,
            datapoint: Union[float, int],
            type_: Optional[str] = None,
            interval: Optional[int] = None,
            tags: List[str] = [],
            api_key: Optional[str] = None,
            app_key: Optional[str] = None,
            datadog_conn_id: str = 'datadog_default',
            **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.api_key = api_key
        self.app_key = app_key
        self.datadog_conn_id = datadog_conn_id
        self.name_metric = name_metric
        self.datapoint = datapoint
        self.tags = tags
        self.type_ = type_
        self.interval = interval

    def execute(self, context: Dict[str, Any]) -> None:
        hook = DatadogHook(
            datadog_conn_id=self.datadog_conn_id,
            api_key=self.api_key,
            app_key=self.app_key
        )

        environment = context.get('params')['environment'] if 'environment' in context.get('params') else 'Undefined'
        self.tags = self.tags + ['environment:{0}'.format(environment),
                                 'dag:{0}'.format(context.get('task_instance').dag_id),
                                 'execution_date:{0}'.format(context.get('execution_date').strftime("%Y-%m-%dT%H:%M:%S"))
                                 ]
        hook.send_metric(
            metric_name=self.name_metric,
            datapoint=self.datapoint,
            tags=self.tags,
            type_=self.type_,
            interval=self.interval
        )
