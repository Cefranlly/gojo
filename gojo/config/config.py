from typing import Dict, Any, List
from pydantic.dataclasses import dataclass


@dataclass
class Config:
   check_type: str # database or spark for now
   slack_token: str
   slack_channels: str | List[str]
   source_config: Dict[str, Any]
   data_test_files: str | List[str] | None
   data_test_vars: Dict[str, Any] | List[Dict[str, Any]] | None
