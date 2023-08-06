"""Module that defines custom exceptions for Panetius."""


class KeyErrorTooDeepException(Exception):
    """Raised if the keys in the config.yml are nested too deeply."""


class LoggingDirectoryDoesNotExistException(Exception):
    """Raised if the logging directory does not exist."""


class InvalidPythonException(Exception):
    """Raised if the environement variable Python type is invalid."""
