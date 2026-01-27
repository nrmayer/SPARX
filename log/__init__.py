from .logger import Logger

_GLOBAL_LOGGER = None

def init_global_logger(*, filename:str|None=None, folder:str|None=None) -> None:
    global _GLOBAL_LOGGER
    if filename is None:
        _GLOBAL_LOGGER = Logger.new_file("logs/" if folder is None else folder)
        return
    _GLOBAL_LOGGER = Logger(filename)

def global_logger() -> Logger:
    if _GLOBAL_LOGGER is None: raise Exception("No global logger")
    return _GLOBAL_LOGGER