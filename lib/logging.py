from .setting import Setting
import traceback


def log(caption, *args):
    if Setting().get('debug'):
        print('[LG]' + caption + " :", *args)


def exception(caption, ex: Exception):
    ex_traceback = ex.__traceback__
    log(caption, ''.join(traceback.format_exception(
        ex.__class__,
        ex,
        ex_traceback
        )))
