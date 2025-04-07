import os
import re
import sys
import time
import asyncio

from typing import Callable, Any, NoReturn

from . import wrap

class Logger:
    """Handles writing log entries into a file"""

    timestamp: int
    filename: str

    _file_lock = False

    tasks:list[asyncio.Task] = []


    def __init__(self, filename:str):
        self.filename = filename

        # seconds since epoch
        self.timestamp = time.time()

        self.log(f"filename {self.filename}, timestamp {round(self.timestamp, 4)}", type="INIT")


    @classmethod
    def new_file(cls, log_folder:str) -> "Logger":
        """Creates a new log file in `log_folder` without overwriting previous log files
        
        Parameters
        ----------
        log_folder : `str`
            The folder in which to place the logs

        Returns
        -------
        Logger : `Logger`
            A `Logger` object with `filename` of a new log file
        """

        logs: list[str] = os.listdir(log_folder)
        
        # pick highest log number
        i = 0
        for log in logs:
            # find number in log file name
            digit:list[str] = re.findall(r"log(\d*).txt", log)

            if len(digit) > 0:
                int_dig = int(digit[0])
                if int_dig > i: i = int_dig
        
        # use highest number + 1
        return cls(log_folder+f"log{i+1}.txt")

    def _write(self, text:str) -> None:
        try:
            while self._file_lock: pass
            self._file_lock = True

            # open in append mode
            with open(self.filename, "a") as file:
                file.write(text)
        finally:
            self._file_lock = False

    def log(self, message:str, type:str="INFO") -> None:
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

        # get time since start
        timestamp = round(time.time() - self.timestamp, 4)

        # write to file
        self._write(f"{timestamp}:{type}:{message}\n")

    def info(self, message:str) -> None:
        self.log(message, type="INFO")

    def warning(self, message:str) -> None:
        self.log(message, type="WARNING")

    def critical(self, message:str) -> None:
        self.log(message, type="CRITICAL")

    def exception(self, message:str) -> None:
        self.log(message, type="EXCEPTION")

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

        def decorator(func:Callable) -> Callable:
            @wrap.wrap(func) # copy function attributes to wrapper
            def wrapper(*args, **kwargs) -> Any:
                self.log(message) # log message
                return func(*args, **kwargs) # call original function
            
            return wrapper
        
        return decorator
    

    def async_log_function(self, seconds:int) -> Callable:
        """Runs given function every `seconds` seconds
        
        Parameters
        ----------
        seconds : `int`
            The number of seconds between function calls

        Returns
        -------
        decorator : `Callable`
        """

        def decorator(func:Callable) -> None:
            @wrap.wrap(func)
            async def wrapper(*args, **kwargs) -> NoReturn:
                while True:
                    time.sleep(seconds)
                    func(*args, **kwargs)
            
            self.tasks.append(
                asyncio.create_task(
                   asyncio.run(wrapper()), 
                   name=func.__name__))

        return decorator
    
    def log_exception(self, *, prepend:str="", append:str="", log_traceback:bool=True):
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

        def decorator(func:Callable) -> Callable:
            @wrap.wrap(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.exception(f"{prepend}Caught exception `{str(e)}` in function `{func.__name__}`{append}")
                    if log_traceback: 
                        import traceback # type:ignore
                        type_, text, tb = sys.exc_info()
                        if tb is None: raise e

                        self._write("Traceback (most recent call last):\n")
                        self._write("".join(traceback.extract_tb(tb).format()))
                        self._write(f"{re.findall(r"^<class '(\w*)'>$", str(type_))[0]}: {text}\n")

                    raise e
                
            return wrapper
        
        return decorator

    def clear_tasks(self) -> None:
        # TODO does not work
        for task in self.tasks:
            task.cancel() # type:ignore
        self.tasks = []