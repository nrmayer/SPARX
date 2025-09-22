from .namedlogger import NamedLogger
from .logger import Logger

# static
_eventloggger = None

def set_logger(logger:Logger|None=None):
    global _eventloggger
    if logger is not None:
        _eventloggger = logger
    else:
        _eventloggger = Logger.new_file("logs/")

def get_logger() -> Logger:
    assert _eventloggger is not None
    return _eventloggger

def get_named_logger(name:str) -> NamedLogger:
    assert _eventloggger is not None
    return NamedLogger(_eventloggger, name)