from .setting import Setting
import logging


def get_logger():
    logger = logging.getLogger('LaravelGoto')
    logger.setLevel(logging.INFO)
    return logger


def is_debug():
    return Setting().get('debug')


def info(caption, *args):
    if is_debug():
        logger = get_logger()
        logger.info(f"{caption}: {args}")


def error(caption, *args):
    if is_debug():
        logger = get_logger()
        logger.error(f"{caption}: {args}")


def warn(caption, *args):
    if is_debug():
        logger = get_logger()
        logger.warning(f"{caption}: {args}")


def exception(caption, ex: Exception):
    if is_debug():
        logger = get_logger()
        logger.exception(caption)
