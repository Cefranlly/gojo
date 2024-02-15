
from typing import Dict, Any
from enum import Enum
from config.config import Config
from data_models.base_check_model import BaseCheckResponseModel
from data_monitoring.alerts.slack import SlackDispatcher
from data_monitoring.data_monitoring import DataMonitoring
from data_monitoring.data_check.slack.message_builder import SlackCheckMessageBuilder
from quality_check.quality_check import (
   QualityCheck, SodaQualityCheck, DeequQualityCheck
)
from quality_runner.quality_runner import QualityRunner
from utils.log import get_logger


logger = get_logger(__name__)


class DataCheckType(str, Enum):
   SODA_CHECK = "soda"
   DEEQU_CHECK = "deequ"

_CHECK_TYPES = {
   DataCheckType.SODA_CHECK: SodaQualityCheck(),
   # DataCheckType.DEEQU_CHECK: DeequQualityCheck()
}


class DataMonitoringChecker(DataMonitoring):

   config: Config
   check_config: Dict[str, Any]
   quality_check: QualityCheck
   quality_runner: QualityRunner

   def __init__(self, config: Config) -> None:
      self.check_config = config.test_config
      logger.info(f"print config: {config.test_config}")
      print(f"print config: {self.check_config}")
      self.quality_check = _CHECK_TYPES[config.check_type]
      self.slack_client = SlackDispatcher(slack_config=config.notification_config)

   def get_monitoring_info(self):
      logger.info("Running Data Monitoring Checker")

   def _set_quality_check(self):
      self.quality_runner = QualityRunner(quality_check=self.quality_check)

   def _run_check(self):
      self._set_quality_check()
      self.quality_runner.run_quality_check(config=self.check_config)

   def _populate_data(self) -> BaseCheckResponseModel:
      return self.quality_check.get_results()

   def send_notifications(self, data: BaseCheckResponseModel) -> None:
      slack_msg_builder = SlackCheckMessageBuilder()
      result_data = {
         "data_source": data.default_data_source,
         "has_errors": data.has_errors,
         "has_warnings": data.has_warnings,
         "has_failures": data.has_failures,
         # "logs": data.logs
         }

      input_data = {
         "title": [{"Data freshness test": "Soda Test"}],
         "result": result_data
         }
      self.slack_client.send_alert(data=input_data, slack_builder=slack_msg_builder)

   def run_operations(self) -> None:
      self.get_monitoring_info()
      self._run_check()
      quality_data = self._populate_data()
      logger.info(f"response: {quality_data}")
      self.send_notifications(quality_data)
