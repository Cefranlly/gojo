from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator
from utils.log import get_logger


logger = get_logger(__name__)

SLACK_MESSAGE_ATTACHMENTS_LIMIT = 50

SlackBlockType = Dict[Any, Any]
SlackBlocksType = List[SlackBlockType]


class SlackMessageSchema(BaseModel):
   text: Optional[str] = None
   attachments: Optional[List[Any]] = None
   blocks: Optional[List[Any]] = None

   @validator("attachments", pre=True)
   def validate_attachments(cls, attachments):
      if (
         isinstance(attachments, list)
         and len(attachments) > SLACK_MESSAGE_ATTACHMENTS_LIMIT
      ):
         logger.error(
            f"Slack message attachments limit is {SLACK_MESSAGE_ATTACHMENTS_LIMIT}, but {len(attachments)} attachments were provided. Attachments were removed from the message.\n"
            )
         return None
      return attachments
