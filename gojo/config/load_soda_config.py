import os
from typing import Union
from pathlib import Path
from ruamel.yaml import YAML
from gojo.config.config import Config
from gojo.utils.log import get_logger


logger = get_logger(__name__)


class LoadConfig:

   _DEFAULT_CONFIG_DIR: str = str(Path.home() / ".gojo/")
   _CONFIG_FILE_NAME: str = "config.yml"
   _config: Config

   @property
   def config(self) -> Config:
      return self._config

   def _load_configuration_file(self, file_path: Union[str, None]) -> dict:
      yaml = YAML()
      if file_path:
         if not os.path.exists(file_path):
            logger.error("Configuration path does not exist")
            raise
         else:
            # Load here if the file_path exists
            logger.info(f"Loading file path: {file_path}")
            with open(file_path, 'r') as file:
               config_loaded = yaml.load(file)
      else:
         default_file_path = os.path.join(self._DEFAULT_CONFIG_DIR, self._CONFIG_FILE_NAME)
         logger.info(f"Default file path: {default_file_path}")
         with open(default_file_path, 'r') as file:
            config_loaded = yaml.load(file)

      return config_loaded

   def load_configuration(self, file_path: Union[str, None]):
      # check if the file exists
      config_dict = self._load_configuration_file(file_path)
      self._config = Config(**config_dict)
