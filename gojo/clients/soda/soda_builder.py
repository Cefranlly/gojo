from typing import Union, List, Dict
from soda.scan import Scan
from gojo.utils.log import get_logger


logger = get_logger(__name__)

SODA_TEST_OK = 0	# all checks passed, all good from both runtime and Soda perspective
SODA_TEST_WARNING = 1	# Soda issues a warning on a check(s)
SODA_TEST_FAIL = 2 # Soda issues a failure on a check(s)


def read_files(files_path: str) -> Union[List[str], str]:
   return ""


class SodaBuilder:
   """Loads all the information needed to run a new test
   """

   _soda_scan: Scan

   def __init__(self, soda_scan: Scan) -> None:
      self._soda_scan = soda_scan

   def add_configuration_file(self, file_path: str):
      self._soda_scan.add_configuration_yaml_file(file_path=file_path)

   def add_variables(self, variables: Dict[str, str]):
      self._soda_scan.add_variables(variables)

   def add_sodacl_checks(self, checks_file_path: str):
      # TODO: Improve this to recive file or files or str
      self._soda_scan.add_sodacl_yaml_files(checks_file_path)
