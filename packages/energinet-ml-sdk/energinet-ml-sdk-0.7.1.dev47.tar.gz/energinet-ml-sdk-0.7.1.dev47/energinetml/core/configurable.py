#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[summary]
"""

import json
import os
from dataclasses import asdict, dataclass
from typing import Union

from energinetml.settings import DEFAULT_ENCODING


@dataclass
class Configurable:
    """[summary]"""

    class NotFound(Exception):
        """[summary]"""

        pass

    # Constants
    CONFIG_FILE_NAME = None

    # Members
    path: str

    @classmethod
    def create(cls, path: str, **kwargs) -> "Configurable":
        """[summary]

        Args:
            path (str): [description]

        Returns:
            Configurable: [description]
        """
        obj = cls(path=path, **kwargs)
        obj.save()
        return obj

    @classmethod
    def from_config_file(cls, file_path: str) -> "Configurable":
        """[summary]

        Args:
            file_path (str): [description]

        Returns:
            Configurable: [description]
        """
        with open(file_path, encoding=DEFAULT_ENCODING) as f:
            return cls(path=os.path.split(file_path)[0], **json.load(f))

    @classmethod
    def from_directory(cls, path: str) -> "Configurable":
        """[summary]

        Args:
            path (str): [description]

        Raises:
            RuntimeError: [description]
            cls.NotFound: [description]

        Returns:
            Configurable: [description]
        """
        if cls.CONFIG_FILE_NAME is None:
            raise RuntimeError("Attribute CONFIG_FILE_NAME is None")

        file_pointer = locate_file_upwards(path, cls.CONFIG_FILE_NAME)

        if file_pointer is not None:
            return cls.from_config_file(file_pointer)
        else:
            raise cls.NotFound()

    def get_file_path(self, *relative_path: str) -> str:
        """Returns absolute path to a file at relative_path,
        where relative_path is relative to config file.

        Args:
            *relative_path (str): [description]

        Returns:
            str: [description]
        """

        return os.path.abspath(os.path.join(self.path, *relative_path))

    def get_relative_file_path(self, absolute_path: str) -> str:
        """Provided an absolute file path, returns the path relative
        to config file.

        Args:
            absolute_path (str): [description]

        Returns:
            str: [description]
        """
        return os.path.relpath(absolute_path, self.path)

    def save(self) -> None:
        """Saved config as JSON to filesystem."""
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        with open(
            self.get_file_path(self.CONFIG_FILE_NAME), "w", encoding=DEFAULT_ENCODING
        ) as f:
            d = asdict(self)
            d.pop("path")
            json.dump(d, f, indent=4, sort_keys=True)


def locate_file_upwards(path: str, filename: str) -> Union[str, None]:
    """[summary]

    Args:
        path (str): [description]
        filename (str): [description]

    Returns:
        str: [description]
    """

    def __is_root(_path: str) -> str:
        """[summary]

        Args:
            _path (str): [description]

        Returns:
            str: [description]
        """
        # you have yourself root.
        # works on Windows and *nix paths.
        # does NOT work on Windows shares (\\server\share)
        return os.path.dirname(_path) == _path

    while 1:
        file_pointer = os.path.join(path, filename)
        if os.path.isfile(file_pointer):
            return file_pointer
        elif __is_root(path):
            return None
        else:
            path = os.path.abspath(os.path.join(path, ".."))
