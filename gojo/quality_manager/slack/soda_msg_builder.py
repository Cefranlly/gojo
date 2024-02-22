from typing import List, Any, Union
from gojo.clients.slack.slack_message_builder import SlackMessageBuilder
from gojo.clients.slack.schema import SlackMessageSchema


PASSED=":white_check_mark:"
FAILED=":x:"
WARNING=":warning:"


class SlackSodaMessageBuilder:

   _message_builder: SlackMessageBuilder
   _blocks: List = []

   def __init__(self) -> None:
      self._message_builder = SlackMessageBuilder()

   def _set_header(self, data_source: str, start: str, end: str) -> None:
      self._blocks.append(self._message_builder.create_header_block(msg="Data alert :rotating_light:"))
      self._blocks.append(self._message_builder.create_text_section_block(
         section_msg=f"""data_source: *{data_source}* \n
         scan start: *{start}* \n
         scan end: *{end}* \n
         """
         ))
      self._blocks.append(self._message_builder.create_divider_block())

   def _set_body(self, results: List[Any]) -> None:
      # for check in results["checks"]:
      for check in results:
         result_emoji = ""
         if check['check_result'] == 'pass':
            result_emoji = PASSED
         elif check['check_result'] == 'warning':
            result_emoji = WARNING
         else:
            result_emoji = FAILED

         # then add checks and their results
         self._blocks.append(
            self._message_builder.create_text_section_block(
               section_msg=f""":arrow_forward: Running check -> *{check['definition']}* \n
               result: {check['check_result']} {result_emoji}"""
               )
            )
         self._blocks.append(self._message_builder.create_divider_block())

   def get_slack_message(
         self,
         test_results: dict
         ) -> SlackMessageSchema:
      self._set_header(
         data_source=test_results["data_source"],
         start=test_results["scan_start"],
         end=test_results["scan_end"]
      )
      self._set_body(results=test_results["checks"])
      # TODO: Please review next to be converted to a get_slack_message method
      return SlackMessageSchema(**{"blocks": self._blocks})
