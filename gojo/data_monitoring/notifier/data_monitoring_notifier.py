from config.config import Config
from data_monitoring.data_monitoring import DataMonitoring
from utils.log import get_logger


logger = get_logger(__name__)


class DataMonitoringNotifier(DataMonitoring):

   def __init__(self, config: Config) -> None:
      super().__init__(config)

   def get_monitoring_info(self):
      logger.info("Running Data Monitoring Notifier")

   def _populate_data(self) -> None:
      pass

   def send_notifications(self) -> None:
      pass
