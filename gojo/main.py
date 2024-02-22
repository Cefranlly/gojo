""" cli/entrypoint to interact with our App
"""
import typer
from typing_extensions import Annotated
from pyfiglet import Figlet
from gojo.utils.log import get_logger
# temporal added next lines
import os
from typing import Optional
from gojo.config.load_config import LoadConfig
from gojo.runners.soda_runner import SodaRunner
from gojo.clients.slack.schema import SlackMessageSchema
from gojo.clients.slack.slack_message_builder import SlackMessageBuilder
from gojo.quality_manager.slack.soda_msg_builder import SlackSodaMessageBuilder
from gojo.clients.slack.client import SlackWebClient
from gojo.quality_manager.soda_manager import SodaManager

logger = get_logger(__name__)

# TODO: Add author and more about the App
f = Figlet(font='slant')
print(f.renderText('Welcome to Gojo data quality tool!!'))


app = typer.Typer()


@app.command()
def run_test():
   logger.info("Run quality_runner")


@app.command()
def send_slack_message_test():
   logger.info("send slack message")
   slack_token = os.environ["SLACK_BOT_TOKEN"]
   blocks = []

   message_builder = SlackMessageBuilder()

   blocks.append(message_builder.create_header_block(msg="Data alert :rotating_light:"))
   blocks.append(message_builder.create_divider_block())
   blocks.append(message_builder.create_text_section_block(section_msg=":arrow_forward: *Running tests for: * \n blah blah blah"))
   blocks.append(message_builder.create_divider_block())
   blocks.append(message_builder.create_text_section_block(section_msg="*Results:* \n"))
   blocks.append(message_builder.create_fields_section_block(section_msgs=["Test 1 :white_check_mark: \n", "Test 2 :x: \n", "Test 3 :warning: \n"]))
   blocks.append(message_builder.create_divider_block())

   messages = SlackMessageSchema(**{"blocks": blocks})

   slack_cli = SlackWebClient(token=slack_token)
   slack_cli.send_message(
      channel="data-quality-notifications",
      message=messages
      )

@app.command()
def load_config_test(config_file_path: Annotated[Optional[str], typer.Argument()] = None):
   config_loaded = LoadConfig()
   config_loaded.load_configuration(config_file_path)
   config = config_loaded.config
   logger.info(f"config loaded: {config}")


@app.command()
def run_soda_test(config_file_path: Annotated[Optional[str], typer.Argument()] = None):
   config_loaded = LoadConfig()
   config_loaded.load_configuration(config_file_path)
   config = config_loaded.config
   logger.info("config loaded")
   soda_runner = SodaRunner(source_name="conversenow")
   soda_runner.set_config(config)
   soda_runner.run()
   results = soda_runner.return_results()
   logger.info(f"results: {results}")


@app.command()
def run_and_send_soda(config_file_path: Annotated[Optional[str], typer.Argument()] = None):
   soda_manager = SodaManager(source_name="conversenow")
   soda_manager.set_config(config_file_path=config_file_path)
   soda_manager.set_checks()
   soda_manager.run_checks()
   soda_manager.send_notifications()
