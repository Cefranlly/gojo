from abc import ABC, abstractmethod
from config.config import Config
from data_models.base_check_model import BaseCheckResponseModel


class DataMonitoring(ABC):
   def __init__(self,
                config: Config
                ) -> None:
      self.config = config

   @abstractmethod
   def get_monitoring_info(self) -> None:
      raise NotImplementedError

   @abstractmethod
   def _populate_data(self) -> BaseCheckResponseModel | None:
      raise NotImplementedError

   @abstractmethod
   def send_notifications(self, data: BaseCheckResponseModel) -> None:
      raise NotImplementedError
