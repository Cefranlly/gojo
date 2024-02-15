from typing import Optional, Dict
from clients.slack.schema import SlackBlocksType, SlackMessageSchema
from clients.slack.slack_message_builder import SlackMessageBuilder, MessageColor


STATUS_DISPLAYS: Dict[str, Dict] = {
    "fail": {"color": MessageColor.RED, "display_name": "Failure"},
    "warn": {"color": MessageColor.YELLOW, "display_name": "Warning"},
    "error": {"color": MessageColor.RED, "display_name": "Error"},
}

class SlackCheckMessageBuilder(SlackMessageBuilder):

   def __init__(self) -> None:
      super().__init__()

   def get_slack_message(
         self,
         title: Optional[SlackBlocksType],
         result: Optional[SlackBlocksType]
         ) -> SlackMessageSchema:
      self._create_slack_alert(title=title, result=result)
      return super().get_slack_message()

   def _create_slack_alert(
         self,
         title: Optional[SlackBlocksType],
         result: Optional[SlackBlocksType]
         ) -> None:
      # self.add_title_to_slack_alert(title)
      self.add_details_to_slack_alert(result)

   def add_title_to_slack_alert(self, title_block: Optional[SlackBlocksType]):

      # self.add_message_color(self._get_color(None))

      self.create_header_block("Data freshness test")
      """if title_block:
         title = [*title_block, self.create_divider_block()]
         self._add_always_displayed_blocks(title)"""

   def add_details_to_slack_alert(
         self,
         result: Optional[SlackBlocksType] = None
         ):
      if result:
         result_blocks = [
               self.create_text_section_block(f"{key}:{value}") for key, value in result.items()
         ]
         self._add_blocks_as_attachments(result_blocks)

   @staticmethod
   def _get_color(alert_status: Optional[str]) -> MessageColor:
        if alert_status is None:
            return MessageColor.RED
        return STATUS_DISPLAYS.get(alert_status, {}).get("color", MessageColor.RED)
