from typing import Callable, override

from .logger import Logger

class NamedLogger:
    """Ties a specified name to each created log"""

    logger:Logger
    name:str

    def __init__(self, logger:Logger, name:str):
        self.logger = logger
        self.name = name
    
    def log(self, message:str, type="INFO") -> None:
        """Writes `message` to the log file

        Parameters
        ----------
        message : `str`
            The message to log
        type : `str` default `"INFO"`
            The type of the message
            Prepended to the log

        Returns
        -------
        `None`
        """
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
        """Logs any exceptions that occur in the decorated function.

        Rethrows the exception once caught
        
        Parameters
        ----------
        prepend : `str` default `""`
            String to prepend to log message
        append : `str` default `""`
            String to append to log message
        log_traceback : `bool` default `True`
            Whether to log the full traceback after the exception

        Returns
        -------
        decorator : `Callable`
        """
        return self.logger.log_exception(prepend=f"{self.name}:{prepend}", append=append)
    
    def function_message(self, message:str) -> Callable:
        """Logs a message on each function call
        
        Parameters
        ----------
        message : `str`
            The message to print to the log

        Returns
        -------
        decorator : `Callable`
        """
        return self.logger.function_message(message)