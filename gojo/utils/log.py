import logging
import sys


class ColoredFormatter(logging.Formatter):
   YELLOW = "\x1b[33;20m"
   RED = "\x1b[31;20m"
   BOLD_RED = "\x1b[31;1m"
   RESET = "\x1b[0m"
   FORMAT = "%(asctime)s — %(levelname)s — %(message)s"
   DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

   FORMATS = {
      logging.WARNING: YELLOW + FORMAT + RESET,
      logging.ERROR: RED + FORMAT + RESET,
      logging.CRITICAL: BOLD_RED + FORMAT + RESET,
   }

   def format(self, record):
      log_fmt = self.FORMATS.get(record.levelno, self.FORMAT)
      formatter = logging.Formatter(log_fmt, self.DATE_FORMAT)
      return formatter.format(record)


FORMATTER = ColoredFormatter()


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.INFO)
    return console_handler


def get_logger(logger_name: str):
    set_root_logger_handlers(logger_name)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    return logger


def set_root_logger_handlers(logger_name: str) -> None:
    logger = logging.getLogger(logger_name)
    logger.addHandler(get_console_handler())
