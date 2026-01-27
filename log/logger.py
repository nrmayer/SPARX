import time
import os
import re

FORMAT_STR = "{timestamp} | {type} | {message}"

TYPE_STRINGS = {
    "info": "INFO",
    "warning": "WARN",
    "error": "ERR",
}

class Logger:
    filename: str
    format_str = FORMAT_STR
    type_strings = TYPE_STRINGS
    
    # can't type because micropython doesn't have typing module
    file_handler = None 

    def __init__(self, filename:str):
        self.filename = filename
        self.file_handler = open(filename, "w+")

    def __del__(self):
        if self.file_handler is not None: 
            self.file_handler.close()

    def _write_file(self, txt:str) -> None:
        if self.file_handler is None: raise Exception("No `Logger` file handler")
        self.file_handler.write(txt)

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
            re_match = re.compile("log(\\d*).txt").match(log)
            if re_match is None: continue

            digit:str = re_match.group(0)

            if len(digit) > 0:
                int_dig = int(digit)
                if int_dig > i: i = int_dig

        # add trailing / if it's not there
        if log_folder[-1] != "/": log_folder += "/"

        # use highest number + 1
        return cls(log_folder+f"log{i+1}.txt")

    def set_format_string(self, string:str) -> None:
        """Sets the log format string of the logger
        
        Parameters
        ----------
        string : `str`
            Format string, using string.format() builtin method

        Returns
        -------
        None : `None`
        """

        self.format_str = string

    def set_type_string(self, key:str, val:str) -> None:
        self.type_strings[key] = val

    def write_log(self, type_:str, message:str, **kwargs) -> None:
        self._write_file(
            self.format_str.format(
                timestamp = time.ticks_ms(),
                type = type_ if type_ not in self.type_strings.keys() else self.type_strings[type_],
                message = message,
                **kwargs
            )
        )

    def write_info(self, message:str, **kwargs) -> None:
        self.write_log("info", message, **kwargs)

    def write_warning(self, message:str, **kwargs) -> None:
        self.write_log("warning", message, **kwargs)

    def write_error(self, message:str, **kwargs) -> None:
        self.write_log("error", message, **kwargs)