# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panaetius', 'panaetius.utilities']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'panaetius',
    'version': '2.3.3',
    'description': 'Python module to gracefully handle a .config file/environment variables for scripts, with built in masking for sensitive options. Provides a Splunk friendly formatted logger instance.',
    'long_description': '# Panaetius\n\nThis package provides:\n\n- Functionality to read user variables from a `config.yml` or environment variables.\n- A convenient default logging formatter printing `json` that can save to disk and rotate.\n- Utility functions.\n\n## Config\n\n### options\n\n#### skip_header_init\n\nIf `skip_header_init=True` then the `config_path` will not use the `header_variable` as the\nsub-directory in the `config_path`.\n\nE.g\n\n`CONFIG = panaetius.Config("tembo", "~/tembo/.config", skip_header_init=True)`\n\nWill look in `~/tembo/config/config.yml`.\n\nIf `skip_header_init=False` then would look in `~/tembo/config/tembo/config.yml`.\n\n### Module\n\nConvenient to place in a package/sub-package `__init__.py`.\n\nSee Tembo for an example: <https://github.com/tembo-pages/tembo-core/blob/main/tembo/cli/__init__.py>\n\nExample snippet to use in a module:\n\n```python\n"""Subpackage that contains the CLI application."""\n\nimport os\nfrom typing import Any\n\nimport panaetius\nfrom panaetius.exceptions import LoggingDirectoryDoesNotExistException\n\n\nif (config_path := os.environ.get("TEMBO_CONFIG")) is not None:\n    CONFIG: Any = panaetius.Config("tembo", config_path, skip_header_init=True)\nelse:\n    CONFIG = panaetius.Config(\n        "tembo", "~/tembo/.config", skip_header_init=True\n    )\n\n\npanaetius.set_config(CONFIG, "base_path", "~/tembo")\npanaetius.set_config(CONFIG, "template_path", "~/tembo/.templates")\npanaetius.set_config(CONFIG, "scopes", {})\npanaetius.set_config(CONFIG, "logging.level", "DEBUG")\npanaetius.set_config(CONFIG, "logging.path")\n\ntry:\n    logger = panaetius.set_logger(\n        CONFIG, panaetius.SimpleLogger(logging_level=CONFIG.logging_level)\n    )\nexcept LoggingDirectoryDoesNotExistException:\n    _LOGGING_PATH = CONFIG.logging_path\n    CONFIG.logging_path = ""\n    logger = panaetius.set_logger(\n        CONFIG, panaetius.SimpleLogger(logging_level=CONFIG.logging_level)\n    )\n    logger.warning("Logging directory %s does not exist", _LOGGING_PATH)\n\n```\n\nThis means in `./tembo/cli/cli.py` you can\n\n```python\nimport tembo.cli\n\n# access the CONFIG instance + variables from the config.yml\ntembo.cli.CONFIG\n```\n\n\n## Utility Functions\n\n### Squasher\n\nSquashes a json object or Python dictionary into a single level dictionary.\n',
    'author': 'dtomlinson',
    'author_email': 'dtomlinson@panaetius.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dtomlinson91/panaetius',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
