from .logger import Logger

_GLOBAL_LOGGER = None

def init_global_logger(*, filename:str|None=None, folder:str|None=None) -> None:
    """Initializes global logger, which can be accessed through `global_logger()`
    Ideally, should only be called once
        
    Parameters
    ----------
    filename : `str | None`
        The log's filename\n
        If `None` a new log will be generated in `folder` without overwriting previous logs
    folder : `str | None`
        The folder in which to place the log\n
        If `None` cwd will be used

    Returns
    -------
    None : `None`
    """

    global _GLOBAL_LOGGER
    if filename is None:
        _GLOBAL_LOGGER = Logger.new_file("logs/" if folder is None else folder)
        return
    _GLOBAL_LOGGER = Logger(filename)

def global_logger() -> Logger:
    """Retrieves global logger, which must first be initialized through `init_global_logger()`
        
    Parameters
    ----------
    None

    Returns
    -------
    GLOBAL_LOGGER : `Logger`
    """

    if _GLOBAL_LOGGER is None: raise Exception("No global logger")
    return _GLOBAL_LOGGER