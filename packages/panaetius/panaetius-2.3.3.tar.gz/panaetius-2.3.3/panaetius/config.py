"""
Config module to access variables from a config file or an environment variable.

This module defines the `Config` class to interact and read variables from either a
`config.yml` or an environment variable.
"""

from __future__ import annotations

import ast
import os
import pathlib
from typing import Any

# import toml
import yaml

from panaetius.exceptions import KeyErrorTooDeepException


class Config:
    """
    A configuration class to access user variables.

    Args:
        header_variable (str): the `header` variable.
        config_path (str|None=None): the path where the header directory is stored.
        skip_header_init (bool=False): if True will not use a header subdirectory in the
            `config_path`.

    """

    def __init__(
        self,
        header_variable: str,
        config_path: str | None = None,
        skip_header_init: bool = False,
    ) -> None:
        """
        Create a Config object to set and access variables.

        Args:
            header_variable (str): Your header variable name.
            config_path (str, optional): The path where the header directory is stored.
                Defaults to None on initialisation.
            skip_header_init (bool, optional): If True will not use a header
                subdirectory in the `config_path`. Defaults to False.

        Examples:
            `config_path` defaults to None on initialisation but will be set to `~/.config`.

            A header of `data_analysis` with a config_path of `~/myapps` will define
                a config file in `~/myapps/data_analysis/config.yml`.
        """
        self.header_variable = header_variable
        self.config_path = (
            pathlib.Path(config_path).expanduser()
            if config_path is not None
            else pathlib.Path.home() / ".config"
        )
        self.skip_header_init = skip_header_init
        self._missing_config = self._check_config_file_exists()

        # default logging options
        self.logging_path: str | None = None
        self.logging_rotate_bytes: int = 0
        self.logging_backup_count: int = 0

    @property
    def config(self) -> dict:
        """
        Return the contents of the config file.

        If no config file is specified then this returns an empty dictionary.

        Returns:
            dict: The contents of the config `.yml` loaded as a python dictionary.
        """
        if self.skip_header_init:
            config_file_location = self.config_path / "config.yml"
        else:
            config_file_location = self.config_path / self.header_variable / "config.yml"
        try:
            with open(config_file_location, "r", encoding="utf-8") as config_file:
                # return dict(toml.load(config_file))
                return dict(yaml.load(stream=config_file, Loader=yaml.SafeLoader))
        except FileNotFoundError:
            return {}

    def get_value(self, key: str, default: Any) -> Any:
        """
        Get the value of a variable from the key name.

        The key can either be one (`value`) or two (`data.value`) levels deep.

        A key of `value` (with a header of `data_analysis`) would refer to a
        `config.yml` of:

        ```
        [data_analysis]
        value = "some value"
        ```

        or an environment variable of `DATA_ANALYSIS_VALUE="'some value'"`.

        A key of `data.value` would refer to a `config.yml` of:
        ```
        [data_analysis.data]
        value = "some value"
        ```
        or an environment variable of `DATA_ANALYSIS_DATA_VALUE="'some value'"`.

        Args:
            key (str): The key of the variable.
            default (Any): The default value if the key cannot be found in the config
                file, or an environment variable.

        Returns:
            Any: The value of the variable.
        """
        env_key = f"{self.header_variable.upper()}_{key.upper().replace('.', '_')}"

        if not self._missing_config:
            # look in the config file
            return self._get_config_value(env_key, key, default)
        # no config file, look for env vars
        return self._get_env_value(env_key, default)

    def _check_config_file_exists(self) -> bool:
        if self.skip_header_init is False:
            config_file_location = self.config_path / self.header_variable / "config.yml"
        else:
            config_file_location = self.config_path / "config.yml"
        try:
            with open(config_file_location, "r", encoding="utf-8"):
                return False
        except FileNotFoundError:
            return True

    def _get_config_value(self, env_key: str, key: str, default: Any) -> Any:
        try:
            # look under top header
            # REVIEW: could this be auto handled for a key of arbitrary length?

            # check for env variable and have it take priority
            value = os.environ.get(env_key.replace("-", "_"))
            if value is not None:
                return self.__get_config_value_env_var_override(value)

            if len(key.split(".")) > 2:
                raise KeyErrorTooDeepException(
                    f"Your key of {key} can only be 2 levels deep maximum. "
                    f"You have {len(key.split('.'))}"
                )
            if len(key.split(".")) == 1:
                return self.__get_config_value_key_split_once(key)
            if len(key.split(".")) == 2:
                return self.__get_config_value_key_split_twice(key)
            raise KeyError()

        except (KeyError, TypeError):
            if value is None:
                return self.__get_config_value_missing_key_value_is_none(default)
            # if env var is present, load it
            return self.__get_config_value_missing_key_value_is_not_none(value)

    def __get_config_value_key_split_once(self, key: str) -> Any:
        name = key.lower()
        return self.config[self.header_variable][name]

    def __get_config_value_key_split_twice(self, key: str) -> Any:
        section, name = key.lower().split(".")
        return self.config[self.header_variable][section][name]

    def __get_config_value_missing_key_value_is_none(self, default: Any) -> Any:
        return self.__load_default_value(default)

    def __get_config_value_missing_key_value_is_not_none(self, value: str) -> Any:
        return self.__load_value(value)

    def __get_config_value_env_var_override(self, value: str) -> Any:
        return self.__load_value(value)

    def _get_env_value(self, env_key: str, default: Any) -> Any:  # noqa
        # look for an environment variable, fallback to default
        value = os.environ.get(env_key.replace("-", "_"))
        if value is None:
            return self.__load_default_value(default)
        return self.__load_value(value)

    def __load_value(self, value: str) -> Any:  # noqa
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            # string without spaces: ValueError, with spaces; SyntaxError
            return value

    def __load_default_value(self, default: Any) -> Any:  # noqa
        return default
