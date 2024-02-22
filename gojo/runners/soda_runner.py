from gojo.clients.soda.soda import SodaCli
from gojo.clients.soda.soda_builder import SodaBuilder
from gojo.config.config import Config
from gojo.parsers.soda_yaml_parser import get_ds_in_yaml_str_format
from gojo.utils.log import get_logger


logger = get_logger(__name__)
"""
Operations:
   - config
   - run
   - gather results
   - notify
"""

class SodaRunner:
   soda_cli: SodaCli
   _soda_builder: SodaBuilder

   def __init__(self, source_name: str) -> None:
      self.soda_cli = SodaCli(source_name=source_name)
      self._soda_builder = SodaBuilder(soda_scan=self.soda_cli.scan)

   def set_config(self, config: Config):
      logger.info("set config - soda")
      data_source_yaml = get_ds_in_yaml_str_format(
         self.soda_cli.scan._data_source_name,
         config.source_config
      )
      self._soda_builder.add_ds_configuration(data_source_yaml)

      if config.data_test_vars:
         logger.info(f"Adding variables: {config.data_test_vars}")
         self._soda_builder.add_variables(config.data_test_vars)

      logger.info("Adding sodacl checks")
      self._soda_builder.add_sodacl_checks(config.data_test_files)

   def run(self) -> None:
      logger.info("Run soda checks")
      self.soda_cli.run_check()

   def _format_output(self, output: dict) -> dict:
      result = {
         "data_source": output["defaultDataSource"],
         "data_timestamp": output["dataTimestamp"],
         "scan_start": output["scanStartTimestamp"],
         "scan_end": output["scanEndTimestamp"],
         "has_errors": output["hasErrors"],
         "has_warnings": output["hasWarnings"],
         "has_failures": output["hasFailures"],
      }

      result.update(
         {
            "checks": [
            {
               "definition": check["definition"].replace("\n", ""),
               "table": check["table"],
               "evaluated_column": check["column"],
               "filter": check["filter"],
               "check_result": check["outcome"],
               "diagnostics": check["diagnostics"]
             }
             for check in output["checks"]
            ]
         }
      )

      return result

   def return_results(self) -> dict:
      logger.info("Return soda results")
      return self._format_output(self.soda_cli.get_check_results())
