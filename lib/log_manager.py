from .setting import Setting
import logging


class LogManager:
    def __init__(self, subject):
        self.subject = subject
        self.logger = self.get_logger()

    def get_logger(self):
        logger = logging.getLogger('LaravelGoto')
        logger.setLevel(logging.INFO)
        return logger

    def is_debug(self):
        return Setting().get('debug')

    def info(self, caption, *args):
        if self.is_debug():
            logger = self.get_logger()
            logger.info(f"{self.subject} - {caption}: {args}")

    def error(self, caption, *args):
        if self.is_debug():
            logger = self.get_logger()
            logger.error(f"{self.subject} - {caption}: {args}")

    def warn(self, caption, *args):
        if self.is_debug():
            logger = self.get_logger()
            logger.warning(f"{self.subject} - {caption}: {args}")

    def exception(self, caption, ex: Exception):
        if self.is_debug():
            logger = self.get_logger()
            logger.exception(f"{self.subject} - {caption}: {ex}")
