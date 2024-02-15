from typing import Union, List
from soda.scan import Scan
from utils.log import get_logger
from data_models.soda_check_model import SodaCheckResponseModel

logger = get_logger(__name__)

SODA_TEST_OK = 0	# all checks passed, all good from both runtime and Soda perspective
SODA_TEST_WARNING = 1	# Soda issues a warning on a check(s)
SODA_TEST_FAIL = 2 # Soda issues a failure on a check(s)


def read_files(files_path: str) -> Union[List[str], str]:
   return ""


class SodaTestCli:

   def __init__(self) -> None:
      self.soda_scan = Scan()
      self.soda_scan.set_verbose(True)
      self.soda_scan.set_data_source_name("conversenow")

   def get_soda_scan(self) -> Scan:
      return self.soda_scan

   def run_scan(self):
      # TODO: Add exceptions handle in here
      exit_code = self.soda_scan.execute()
      logger.info(f"Soda test exit_code: {exit_code}")

   def get_scan_results(self) -> SodaCheckResponseModel:
      # Inspect the scan result
      return SodaCheckResponseModel(**self.soda_scan.get_scan_results())

   def get_scan_logs(self) -> str | None:
      # Inspect the scan logs
      return self.soda_scan.get_logs_text()


"""
# Typical log inspection
##################
scan.assert_no_error_logs()
scan.assert_no_checks_fail()

# Advanced methods to inspect scan execution logs
#################################################
scan.has_error_logs()
scan.get_error_logs_text()

# Advanced methods to review check results details
########################################
scan.get_checks_fail()
scan.has_check_fails()
scan.get_checks_fail_text()
scan.assert_no_checks_warn_or_fail()
scan.get_checks_warn_or_fail()
scan.has_checks_warn_or_fail()
scan.get_checks_warn_or_fail_text()
scan.get_all_checks_text()

"""
