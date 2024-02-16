""" cli/entrypoint to interact with our App
"""
import typer
from pyfiglet import Figlet
from gojo.utils.log import get_logger

# temporal added next lines
import os
from gojo.clients.slack.slack_message_builder import SlackMessageBuilder
from gojo.clients.slack.client import SlackWebClient
from gojo.clients.slack.schema import SlackMessageSchema


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
