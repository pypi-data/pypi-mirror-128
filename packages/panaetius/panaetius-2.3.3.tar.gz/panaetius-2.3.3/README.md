# Panaetius

This package provides:

- Functionality to read user variables from a `config.yml` or environment variables.
- A convenient default logging formatter printing `json` that can save to disk and rotate.
- Utility functions.

## Config

### options

#### skip_header_init

If `skip_header_init=True` then the `config_path` will not use the `header_variable` as the
sub-directory in the `config_path`.

E.g

`CONFIG = panaetius.Config("tembo", "~/tembo/.config", skip_header_init=True)`

Will look in `~/tembo/config/config.yml`.

If `skip_header_init=False` then would look in `~/tembo/config/tembo/config.yml`.

### Module

Convenient to place in a package/sub-package `__init__.py`.

See Tembo for an example: <https://github.com/tembo-pages/tembo-core/blob/main/tembo/cli/__init__.py>

Example snippet to use in a module:

```python
"""Subpackage that contains the CLI application."""

import os
from typing import Any

import panaetius
from panaetius.exceptions import LoggingDirectoryDoesNotExistException


if (config_path := os.environ.get("TEMBO_CONFIG")) is not None:
    CONFIG: Any = panaetius.Config("tembo", config_path, skip_header_init=True)
else:
    CONFIG = panaetius.Config(
        "tembo", "~/tembo/.config", skip_header_init=True
    )


panaetius.set_config(CONFIG, "base_path", "~/tembo")
panaetius.set_config(CONFIG, "template_path", "~/tembo/.templates")
panaetius.set_config(CONFIG, "scopes", {})
panaetius.set_config(CONFIG, "logging.level", "DEBUG")
panaetius.set_config(CONFIG, "logging.path")

try:
    logger = panaetius.set_logger(
        CONFIG, panaetius.SimpleLogger(logging_level=CONFIG.logging_level)
    )
except LoggingDirectoryDoesNotExistException:
    _LOGGING_PATH = CONFIG.logging_path
    CONFIG.logging_path = ""
    logger = panaetius.set_logger(
        CONFIG, panaetius.SimpleLogger(logging_level=CONFIG.logging_level)
    )
    logger.warning("Logging directory %s does not exist", _LOGGING_PATH)

```

This means in `./tembo/cli/cli.py` you can

```python
import tembo.cli

# access the CONFIG instance + variables from the config.yml
tembo.cli.CONFIG
```


## Utility Functions

### Squasher

Squashes a json object or Python dictionary into a single level dictionary.
