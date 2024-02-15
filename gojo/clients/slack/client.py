from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from slack_sdk import WebhookClient
from clients.slack.schema import SlackMessageSchema
from utils.log import get_logger


logger = get_logger(__name__)

OK_STATUS_CODE = 200


class SlackClient(ABC):

   def __init__(self) -> None:
      self.client = self._init_client()

   @abstractmethod
   def _init_client(self):
      raise NotImplementedError

   @staticmethod
   def create_client(config: Dict[str, Any]) -> Optional["SlackClient"]:
      if config["slack_webhook"]:
         return SlackWebhookClient(webhook=config["slack_webhook"])

   @abstractmethod
   def send_message(self, message: SlackMessageSchema, **kwargs) -> bool:
      raise NotImplementedError


class SlackWebhookClient(SlackClient):
   def __init__(self, webhook: str) -> None:
      self.webhook = webhook
      super().__init__()

   def _init_client(self) -> WebhookClient:
      return WebhookClient(
         url=self.webhook, default_headers={"Content-type": "application/json"}
      )

   def send_message(self, message: SlackMessageSchema, **kwargs) -> bool:
      response = self.client.send(
         text="Data freshness test",
         blocks=message.attachments[0]['blocks']
      )

      logger.info(f"send_blocks: {message.blocks}")
      logger.info(f"send_attachments: {message.attachments[0]['blocks']}")

      if response.status_code == OK_STATUS_CODE:
         return True
      else:
         logger.error(
            f"Couldn't send the message to Slack - error: {response.body}"
         )
         return False
