"""Sub-module that defines squashing json objects into a single json object."""

from __future__ import annotations

from copy import deepcopy
import itertools
from typing import Iterator, Tuple


class Squash:
    """Squash a json object or Python dictionary into a single level dictionary."""

    def __init__(self, data: dict) -> None:
        """
        Create a Squash object to squash data into a single level dictionary.

        Args:
            data (dict): [description]

        Example:
            squashed_data = Squash(my_data)

            squashed_data.as_dict
        """
        self.data = data

    @property
    def as_dict(self) -> dict:
        """
        Return the squashed data as a dictionary.

        Returns:
            dict: The original data squashed as a dict.
        """
        return self._squash()

    @staticmethod
    def _unpack_dict(
        key: str, value: dict | list | str
    ) -> Iterator[Tuple[str, dict | list | str]]:
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                temporary_key = f"{key}_{sub_key}"
                yield temporary_key, sub_value
        elif isinstance(value, list):
            for index, sub_value in enumerate(value):
                temporary_key = f"{key}_{index}"
                yield temporary_key, sub_value
        else:
            yield key, value

    def _squash(self) -> dict:
        result = deepcopy(self.data)
        while True:
            result = dict(
                itertools.chain.from_iterable(
                    itertools.starmap(self._unpack_dict, result.items())
                )
            )
            if not any(
                isinstance(value, dict) for value in result.values()
            ) and not any(isinstance(value, list) for value in result.values()):
                break
        return result
