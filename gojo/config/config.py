from typing import Dict, Any

class Config:
   notification_config: Dict[str, Any] = {
      "slack_webhook": "SLACK_WEBHOOK_URL"
   }
   check_type = "soda"
   test_config: Dict[str, Any] = {
      "config_file_path": "./config/credentials/data_source.yml",
      "variables": "2023-01-25",
      "checks_file_path": "./config/checks/test_check.yml"
   }
