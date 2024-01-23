from .setting import Setting
import traceback
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
        logger.info(str(caption) + ':' + str(*args))


def error(caption, *args):
    if is_debug():
        logger = get_logger()
        logger.error(str(caption) + ':' + str(*args))


def warn(caption, *args):
    if is_debug():
        logger = get_logger()
        logger.warning(str(caption) + ':' + str(*args))


def exception(caption, ex: Exception):
    if is_debug():
        logger = get_logger()
        logger.exception(caption)

    # ex_traceback = ex.__traceback__
    # error(caption, ''.join(traceback.format_exception(
    #     ex.__class__,
    #     ex,
    #     ex_traceback
    #     )))
