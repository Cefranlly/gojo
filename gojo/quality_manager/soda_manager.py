import os
from typing import Union
from gojo.utils.log import get_logger
from gojo.config.config import Config
from gojo.config.load_config import LoadConfig
from gojo.quality_manager.slack.soda_msg_builder import SlackSodaMessageBuilder
from gojo.clients.slack.client import SlackWebClient
from gojo.quality_manager.base_manager import BaseManager
from gojo.runners.soda_runner import SodaRunner


logger = get_logger(__name__)


class SodaManager(BaseManager):
   config: Config
   soda_runner: SodaRunner
   msg_builder: SlackSodaMessageBuilder

   def __init__(self, source_name: str) -> None:
      self.config_loader = LoadConfig()
      self.soda_runner = SodaRunner(source_name=source_name)
      self.msg_builder = SlackSodaMessageBuilder()

   def set_config(self, config_file_path: Union[str, None]) -> None:
      logger.info("Load configuration for SODA checks")
      self.config_loader.load_configuration(config_file_path)
      self.config = self.config_loader.config

   def set_checks(self) -> None:
      self.soda_runner.set_config(self.config)

   def run_checks(self) -> None:
      logger.info("Running SODA checks")
      self.soda_runner.run()

   def get_results(self) -> dict | None:
      results = self.soda_runner.return_results()
      logger.info(f"results: {results}")
      return results

   def send_notifications(self) -> None:
      slack_token = self.config.slack_token or os.environ["SLACK_BOT_TOKEN"]
      messages = self.msg_builder.get_slack_message(test_results=self.get_results())

      slack_cli = SlackWebClient(token=slack_token)
      slack_cli.send_message(
         channel=self.config.slack_channels,
         message=messages
         )
