from typing import Dict, Any
from abc import ABC, abstractmethod

from clients.soda.soda import SodaTestCli
from clients.soda.soda_builder import SodaTestBuilder
from data_models.base_check_model import BaseCheckResponseModel

class QualityCheck(ABC):

   @abstractmethod
   def set_configuration(self, config: Dict[str, Any]) -> None:
      raise NotImplementedError

   @abstractmethod
   def run_checks(self) -> None:
      raise NotImplementedError

   @abstractmethod
   def get_results(self) -> BaseCheckResponseModel:
      raise NotImplementedError


class SodaQualityCheck(QualityCheck):

   soda_cli: SodaTestCli
   _soda_test_builder: SodaTestBuilder

   def __init__(self) -> None:
      self.soda_cli = SodaTestCli()

   def set_configuration(
         self,
         config: Dict[str, Any]
      ) -> None:
      self._soda_test_builder = SodaTestBuilder(self.soda_cli.get_soda_scan())
      self._soda_test_builder.add_configuration_file(config['config_file_path'])
      self._soda_test_builder.add_variables({"date": config['variables']})
      self._soda_test_builder.add_sodacl_checks(config['checks_file_path'])

   def run_checks(self):
      self.soda_cli.run_scan()

   def get_results(self) -> BaseCheckResponseModel:
      return self.soda_cli.get_scan_results()

   def get_logs(self) -> str | None:
      return self.soda_cli.get_scan_logs()


class DeequQualityCheck(QualityCheck):
   """Quality check for Spark jobs using Deequ python library

   Args:
       QualityCheck (_type_): _description_
   """
   def __init__(self) -> None:
      pass
