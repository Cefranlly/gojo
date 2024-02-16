from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator
from gojo.utils.log import get_logger


logger = get_logger(__name__)

SLACK_MESSAGE_BLOCKS_LIMIT = 50

SlackBlockType = Dict[Any, Any]
SlackBlocksType = List[SlackBlockType]


class SlackMessageSchema(BaseModel):
   text: Optional[str] = None
   blocks: Optional[List[Any]] = None

   @validator("blocks", pre=True)
   def validate_blocks(cls, blocks):
      if (
         isinstance(blocks, list)
         and len(blocks) > SLACK_MESSAGE_BLOCKS_LIMIT
      ):
         logger.error(
            f"Slack message blocks limit is {SLACK_MESSAGE_BLOCKS_LIMIT}, but {len(blocks)} blocks were provided. Blocks were removed from the message.\n"
            )
         return None
      return blocks
