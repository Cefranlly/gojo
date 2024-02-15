from typing import Dict, Any
from quality_check.quality_check import QualityCheck
from data_models.base_check_model import BaseCheckResponseModel

class QualityRunner:

   quality_check: QualityCheck

   def __init__(self, quality_check: QualityCheck) -> None:
      self.quality_check = quality_check

   def run_quality_check(self, config: Dict[str, Any]) -> BaseCheckResponseModel:
      self.quality_check.set_configuration(config=config)
      self.quality_check.run_checks()
      return self.quality_check.get_results()


   """
   def get_results(self) -> Dict[str, Any]:
      return self.quality_check.get_results()
   """
