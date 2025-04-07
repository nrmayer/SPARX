from .namedlogger import NamedLogger
from .logger import Logger

_EVENTLOGGER = None

def _check_eventlogger():
    if _EVENTLOGGER is None:
        raise Exception("No logger found")

def set_logger(logger:Logger|None=None):
    global _EVENTLOGGER
    if logger is not None:
        _EVENTLOGGER = logger
    else:
        _EVENTLOGGER = Logger.new_file("logs/")

def get_logger() -> Logger:
    _check_eventlogger()
    return _EVENTLOGGER # type:ignore

def get_named_logger(name:str) -> NamedLogger:
    _check_eventlogger()
    return NamedLogger(_EVENTLOGGER, name) # type:ignore