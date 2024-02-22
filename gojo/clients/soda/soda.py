from soda.scan import Scan
from gojo.utils.log import get_logger


logger = get_logger(__name__)

SODA_TEST_OK = 0	# all checks passed, all good from both runtime and Soda perspective
SODA_TEST_WARNING = 1	# Soda issues a warning on a check(s)
SODA_TEST_FAIL = 2 # Soda issues a failure on a check(s)


class SodaCli:

   _soda_scan: Scan

   def __init__(self, source_name: str) -> None:
      self._soda_scan = Scan()
      self._soda_scan.set_verbose(True)
      self._soda_scan.set_data_source_name(source_name)

   @property
   def scan(self) -> Scan:
      return self._soda_scan

   def run_check(self):
      # TODO: Add exceptions handle in here
      exit_code = self._soda_scan.execute()
      logger.info(f"Soda test exit_code: {exit_code}")

   def get_check_results(self) -> dict:
      # Inspect the scan result
      return self._soda_scan.get_scan_results()

   def get_check_logs(self) -> str | None:
      # Inspect the scan logs
      return self._soda_scan.get_logs_text()


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
