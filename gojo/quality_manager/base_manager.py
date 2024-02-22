from abc import ABC, abstractmethod


class BaseManager(ABC):
   @abstractmethod
   def set_config(self) -> None:
      raise NotImplementedError

   @abstractmethod
   def set_checks(self) -> dict | None:
      raise NotImplementedError

   @abstractmethod
   def run_checks(self) -> dict | None:
      raise NotImplementedError

   @abstractmethod
   def get_results(self) -> dict | None:
      raise NotImplementedError

   @abstractmethod
   def send_notifications(self, data: dict) -> None:
      raise NotImplementedError
