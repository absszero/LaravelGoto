from .setting import Setting
import traceback


def debug(caption, *args):
    if Setting().get('debug'):
        print('[LG]' + caption + " :", *args)


def exception(caption, ex: Exception):
    ex_traceback = ex.__traceback__
    debug(caption, ''.join(traceback.format_exception(
        ex.__class__,
        ex,
        ex_traceback
        )))
