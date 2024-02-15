from typing import Dict, Any
from clients.slack.client import SlackClient
from clients.slack.schema import SlackMessageSchema
from clients.slack.slack_message_builder import SlackMessageBuilder
from config.config import Config



class SlackDispatcher:

   slack_client: SlackClient
   message_builder: SlackMessageBuilder

   def __init__(self, slack_config: Config) -> None:
      self.slack_config = slack_config
      self._initial_client()

   def _initial_client(self) -> None:
      self.slack_client = SlackClient.create_client(config=self.slack_config)
      if not self.slack_client:
         raise Exception("Could not initialize Slack client")

   def _get_message(self, data: Dict[str, Any], slack_builder: SlackMessageBuilder) -> SlackMessageSchema:
      return slack_builder.get_slack_message(title=data["title"], result=data["result"])

   def send_alert(self, data: Dict[str, Any], slack_builder: SlackMessageBuilder):
      slack_message = self._get_message(data, slack_builder)
      self.slack_client.send_message(message=slack_message)
