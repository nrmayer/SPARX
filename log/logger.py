"""Implements `Logger` class, which handles log files

Opens specified file, and tracks its file handler

Formats logs, with log types such as warning or error

Automatically timestamps log entries

Able to create a new log in a folder without overwriting previous logs
"""

import time
import os
import re

_DEFAULT_FORMAT_STR = "{timestamp} | {type} | {message}"

_DEFAULT_TYPE_STRINGS = {
    "info": "INFO",
    "warning": "WARN",
    "error": "ERR",
}

class Logger:
    """
    Opens specified file, and tracks its file handler

    Formats logs, with log types such as warning or error

    Automatically timestamps log entries

    Able to create a new log in a folder without overwriting previous logs
    """

    _filename: str
    _format_str = _DEFAULT_FORMAT_STR
    _type_strings = _DEFAULT_TYPE_STRINGS
    
    # can't type file handler because micropython doesn't have typing module
    _file_handler = None 

    def __init__(self, filename:str):
        self._filename = filename
        self._file_handler = open(filename, "w+")

    def __del__(self):
        if self._file_handler is not None: 
            self._file_handler.close()

    def _write_file(self, txt:str) -> None:
        if self._file_handler is None: raise Exception("No `Logger` file handler")
        self._file_handler.write(txt)

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

        self._format_str = string

    def set_type_string(self, key:str, val:str) -> None:
        """Sets the string translation of a log type
        
        Parameters
        ----------
        key : `str`
            The log type (e.g. "warning")
        val : `str`
            The translated string that is put in the log file (e.g. "WARN")

        Returns
        -------
        None : `None`
        """

        self._type_strings[key] = val

    def write_log(self, type_:str, message:str, **kwargs:list[str]) -> None:
        """Writes an entry to the log file
        
        Parameters
        ----------
        type_ : `str`
            Log type (written to beginning of log entry)
        message : `str`
            Message to write to log
        **kwargs : `list[str]`
            Anything else specified in custom format string

        Returns
        -------
        None : `None`
        """

        self._write_file(
            self._format_str.format(
                timestamp = time.ticks_ms(),
                type = type_ if type_ not in self._type_strings.keys() else self._type_strings[type_],
                message = message,
                **kwargs
            )
        )

    def write_info(self, message:str, **kwargs: list[str]) -> None:
        """Writes a log entry of type "info" to the log file
        
        Parameters
        ----------
        message : `str`
            Message to write to log
        **kwargs : `list[str]`
            Anything else specified in custom format string

        Returns
        -------
        None : `None`
        """

        self.write_log("info", message, **kwargs)

    def write_warning(self, message:str, **kwargs: list[str]) -> None:
        """Writes a log entry of type "warning" to the log file
        
        Parameters
        ----------
        message : `str`
            Message to write to log
        **kwargs : `list[str]`
            Anything else specified in custom format string

        Returns
        -------
        None : `None`
        """

        self.write_log("warning", message, **kwargs)

    def write_error(self, message:str, **kwargs: list[str]) -> None:
        """Writes a log entry of type "error" to the log file
        
        Parameters
        ----------
        message : `str`
            Message to write to log
        **kwargs : `list[str]`
            Anything else specified in custom format string

        Returns
        -------
        None : `None`
        """

        self.write_log("error", message, **kwargs)