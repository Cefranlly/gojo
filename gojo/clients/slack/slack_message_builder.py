from enum import Enum
from typing import List, Dict, Any, Union
from clients.slack.schema import SlackBlocksType, SlackMessageSchema

from slack_sdk.models.blocks import SectionBlock

class MessageColor(Enum):
   YELLOW = "#ffcc00"
   RED = "#ff0000"


class SlackMessageBuilder:
   _LONGEST_MARKDOWN_SUFFIX_LEN = 3
   _CONTINUATION_SYMBOL = "..."
   _MAX_SLACK_SECTION_SIZE = 2
   _MAX_ALERT_PREVIEW_BLOCKS = 5
   _MAX_AMOUNT_OF_ATTACHMENTS = 50
   _HASHTAG = "#"

   def __init__(self) -> None:
      self.slack_message = self._initial_slack_message()

   @classmethod
   def _initial_slack_message(cls) -> Dict[Any, Any]:
      return {"blocks": [], "attachments": [{"blocks": []}]}

   def reset_slack_message(self):
        self.slack_message = self._initial_slack_message()

   def _add_always_displayed_blocks(self, blocks: SlackBlocksType):
        # In oppose to attachments Blocks are always displayed, use this for parts that should always be displayed in the message
        self.slack_message["blocks"].extend(blocks)

   def _add_blocks_as_attachments(self, blocks: SlackBlocksType):
        # The first 5 attachments Blocks are always displayed.
        # The rest of the attachments Blocks are hidden behind "show more" button.
        # NOTICE: attachments blocks are deprecated by Slack.
        self.slack_message["attachments"][0]["blocks"].extend(blocks)

   @property
   def blocks(self) -> List:
      return self.slack_message.get("blocks", [])

   @property
   def attachments(self) -> List:
      return self.slack_message.get("attachments", [])

   @staticmethod
   def get_limited_markdown_msg(section_msg: str) -> str:
        if len(section_msg) < SectionBlock.text_max_length:
            return section_msg
        return (
            section_msg[
                : SectionBlock.text_max_length
                - len(SlackMessageBuilder._CONTINUATION_SYMBOL)
                - SlackMessageBuilder._LONGEST_MARKDOWN_SUFFIX_LEN
            ]
            + SlackMessageBuilder._CONTINUATION_SYMBOL
            + section_msg[-SlackMessageBuilder._LONGEST_MARKDOWN_SUFFIX_LEN :]
        )

   @staticmethod
   def create_divider_block() -> Dict[Any, Any]:
      return {"type": "divider"}

   @staticmethod
   def create_fields_section_block(section_msgs: List) -> Dict[Any, Any]:
      fields = []
      for section_msg in section_msgs:
         fields.append(
               {
                  "type": "mrkdwn",
                  "text": SlackMessageBuilder.get_limited_markdown_msg(section_msg),
               }
         )

      return {"type": "section", "fields": fields}

   @staticmethod
   def create_text_section_block(section_msg: str) -> Dict[Any, Any]:
      return {
         "type": "section",
         "text": {
               "type": "mrkdwn",
               "text": SlackMessageBuilder.get_limited_markdown_msg(section_msg),
         },
      }

   @staticmethod
   def create_empty_section_block() -> Dict[Any, Any]:
      return {
         "type": "section",
         "text": {
               "type": "mrkdwn",
               "text": SlackMessageBuilder.get_limited_markdown_msg("\t"),
         },
      }

   @staticmethod
   def create_context_block(context_msgs: List) -> Dict[Any, Any]:
      fields = []
      for context_msg in context_msgs:
         fields.append(
               {
                  "type": "mrkdwn",
                  "text": SlackMessageBuilder.get_limited_markdown_msg(context_msg),
               }
         )

      return {"type": "context", "elements": fields}

   @staticmethod
   def create_header_block(msg: str) -> Dict[Any, Any]:
      return {
         "type": "header",
         "text": {
               "type": "plain_text",
               "text": msg,
         },
      }

   @staticmethod
   def create_button_action_block(text: str, url: str) -> Dict[Any, Any]:
      return {
         "type": "actions",
         "elements": [
               {
                  "type": "button",
                  "text": {"type": "plain_text", "text": text, "emoji": True},
                  "value": text,
                  "url": url,
               }
         ],
      }

   @staticmethod
   def create_section_with_button(
      section_text: str, button_text: str, url: str
   ) -> Dict[Any, Any]:
      return {
         "type": "section",
         "text": {"type": "mrkdwn", "text": section_text},
         "accessory": {
               "type": "button",
               "text": {"type": "plain_text", "text": button_text, "emoji": True},
               "url": url,
         },
      }

   @staticmethod
   def create_compacted_sections_blocks(section_msgs: List) -> List[Dict[Any, Any]]:
      # Compacting sections into attachments.
      # Each section can contain _MAX_SLACK_SECTION_SIZE fields.
      attachments = []
      section_fields: List[Dict[Any, Any]] = []

      for section_msg in section_msgs:
         section_field = {
               "type": "mrkdwn",
               "text": SlackMessageBuilder.get_limited_markdown_msg(section_msg),
         }
         if len(section_fields) < SlackMessageBuilder._MAX_SLACK_SECTION_SIZE:
               section_fields.append(section_field)
         else:
               attachment = {"type": "section", "fields": section_fields}
               attachments.append(attachment)
               section_fields = [section_field]

      attachment = {"type": "section", "fields": section_fields}
      attachments.append(attachment)
      return attachments

   def get_slack_message(self, *args, **kwargs) -> SlackMessageSchema:
      return SlackMessageSchema(**self.slack_message)

   @staticmethod
   def prettify_and_dedup_List(str_List: Union[List[str], str]) -> str:
      """
      Receives a List of strings, either JSON dumped or not, dedups and sorts it, and returns it as a comma-separated
      string.
      This is useful for various Lists we include in Slack messages (owners, subscribers, etc.)
      """
      if isinstance(str_List, str):
         str_List = unpack_and_flatten_str_to_List(str_List)
      return ", ".join(sorted(set(str_List)))

   def add_message_color(self, color: MessageColor):
      for block in self.blocks:
         block["color"] = color.value
      for attachment in self.attachments:
         attachment["color"] = color.value
