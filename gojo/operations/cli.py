from config.config import Config
from data_monitoring.data_check.data_monitoring_checker import \
    DataMonitoringChecker
from utils.log import get_logger

logger = get_logger(__name__)


""" Entrypoint to run test"""
def quality_runner():
   config = Config # TODO: change this to a module
   logger.info(config.check_type)
   print(config.check_type)
   data_monitoring = DataMonitoringChecker(config=config)
   data_monitoring.run_operations()
