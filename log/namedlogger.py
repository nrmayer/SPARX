from typing import Callable

from .logger import Logger

class NamedLogger:
    """Ties a name to each log created by it

    Is not directly descended from `Logger`, instead uses
    the internal variable `logger:Logger` to write to logs, 
    preserving filename and file lock status"""

    logger:Logger
    name:str

    def __init__(self, logger:Logger, name:str):
        self.logger = logger
        self.name = name

    def log(self, message:str, type="INFO") -> None:
        self.logger.log(f"{self.name}:{message}", type=type)

    def info(self, message:str) -> None:
        self.log(message, type="INFO")

    def warning(self, message:str) -> None:
        self.log(message, type="WARNING")

    def critical(self, message:str) -> None:
        self.log(message, type="CRITICAL")

    def exception(self, message:str) -> None:
        self.log(message, type="EXCEPTION")

    def log_exception(self, prepend:str="", append:str="") -> Callable:
        return self.logger.log_exception(prepend=f"{self.name}:{prepend}", append=append)