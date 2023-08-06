"""Module to provide functionality when interacting with variables."""

from __future__ import annotations

from typing import Any

from panaetius import Config


def set_config(
    config_inst: Config,
    key: str,
    default: Any = None,
) -> None:
    """
    Define a variable to be read from a `config.toml` or an environment variable.

    Args:
        config_inst (Config): The instance of the `Config` class.
        key (str): The key of the variable.
        default (Any, optional): The default value if the key cannot be found in the config
            file, or an environment variable. Defaults to None.

    Example:
        `set_config(CONFIG, "value", default=[1, 2])` would look for a
        `config.toml` with the following structure (with `CONFIG` having a header of
        `data_analysis`):

        ```
        [data_analysis]
        value = "some value"
        ```

        Or an environment variable of `DATA_ANALYSIS_VALUE="'some value'"`.

        If found, this value can be access with `CONFIG.value` which would return
        `some_value`.

        If neither the environment variable nor the `config.toml` are present, the
        default of `[1, 2]` would be returned instead.
    """
    config_var = key.lower().replace(".", "_")
    setattr(config_inst, config_var, config_inst.get_value(key, default))
