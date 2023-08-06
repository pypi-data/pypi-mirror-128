"""Module to define a convenient logger instance with json formatted output."""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
import logging
from logging.handlers import RotatingFileHandler
import pathlib
import sys

from panaetius import Config
from panaetius.library import set_config
from panaetius.exceptions import LoggingDirectoryDoesNotExistException


def set_logger(config_inst: Config, logging_format_inst: LoggingData) -> logging.Logger:
    """
    Set and return a `logging.Logger` instance for quick logging.

    `logging_format_inst` should be an instance of either SimpleLogger, AdvancedLogger,
    or CustomLogger.

    SimpleLogger and AdvancedLogger define a logging format and a logging level info.

    CustomLogger defines a logging level info and should have a logging format passed
    in.

    Logging to a file is defined by a `logging.path` key set on `Config`. This path
    should exist as it will not be created.

    Args:
        config_inst (Config): The instance of the `Config` class.
        logging_format_inst (LoggingData): The instance of the `LoggingData` class.

    Raises:
        LoggingDirectoryDoesNotExistException: If the logging directory specified does
            not exist.

    Returns:
        logging.Logger: An configured instance of `logging.Logger` ready to be used.

    Example:

        ```
        logger = set_logger(CONFIG, SimpleLogger())

        logger.info("some logging message")
        ```

        Would create a logging output of:

        ```
        {
            "time": "2021-10-18 02:26:24,037",
            "logging_level":"INFO",
            "message": "some logging message"
        }
        ```

    """
    logger = logging.getLogger(config_inst.header_variable)
    log_handler_sys = logging.StreamHandler(sys.stdout)

    # configure file handler
    if config_inst.logging_path is not None:
        if not config_inst.skip_header_init:
            logging_file = (
                pathlib.Path(config_inst.logging_path)
                / config_inst.header_variable
                / f"{config_inst.header_variable}.log"
            ).expanduser()
        else:
            logging_file = (
                pathlib.Path(config_inst.logging_path)
                / f"{config_inst.header_variable}.log"
            ).expanduser()

        if not logging_file.parents[0].exists():
            raise LoggingDirectoryDoesNotExistException()

        if config_inst.logging_rotate_bytes == 0:
            set_config(config_inst, "logging.rotate_bytes", 512000)
        if config_inst.logging_backup_count == 0:
            set_config(config_inst, "logging.backup_count", 3)

        log_handler_file = RotatingFileHandler(
            str(logging_file),
            "a",
            config_inst.logging_rotate_bytes,
            config_inst.logging_backup_count,
        )

        log_handler_file.setFormatter(logging.Formatter(logging_format_inst.format))
        logger.addHandler(log_handler_file)

    # configure stdout handler
    log_handler_sys.setFormatter(logging.Formatter(logging_format_inst.format))
    logger.addHandler(log_handler_sys)
    logger.setLevel(logging_format_inst.logging_level)
    return logger


class LoggingData(metaclass=ABCMeta):
    @property
    @abstractmethod
    def format(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def logging_level(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __init__(self, logging_level: str):
        raise NotImplementedError


class SimpleLogger(LoggingData):
    @property
    def format(self) -> str:
        return str(
            '{\n\t"time": "%(asctime)s",\n\t"logging_level":'
            '"%(levelname)s",\n\t"message": "%(message)s"\n}',
        )

    @property
    def logging_level(self) -> str:
        return self._logging_level

    def __init__(self, logging_level: str = "INFO"):
        self._logging_level = logging_level


class AdvancedLogger(LoggingData):
    @property
    def format(self) -> str:
        return str(
            '{\n\t"time": "%(asctime)s",\n\t"file_name": "%(filename)s",'
            '\n\t"module": "%(module)s",\n\t"function":"%(funcName)s",\n\t'
            '"line_number": "%(lineno)s",\n\t"logging_level":'
            '"%(levelname)s",\n\t"message": "%(message)s"\n}',
        )

    @property
    def logging_level(self) -> str:
        return self._logging_level

    def __init__(self, logging_level: str = "INFO"):
        self._logging_level = logging_level


class CustomLogger(LoggingData):
    @property
    def format(self) -> str:
        return str(self._format)

    @property
    def logging_level(self) -> str:
        return self._logging_level

    def __init__(self, logging_format: str, logging_level: str = "INFO"):
        self._logging_level = logging_level
        self._format = logging_format
