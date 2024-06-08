# pylint: disable = unspecified-encoding

"""
Common system utilities such as removing files and getting system variable
"""

import os
import shutil
from typing import Union


def get_sys_var(env_name: str):
    """
    Return the value of a system variable.
    """
    return os.environ.get(env_name.upper())


def remove_f(paths: Union[list[str], str]) -> None:
    """
    Delete the specified paths.

    Paths can be either:
    - a file or a folder.
    - a list of files and/or folders.
    """
    # If a single path is given, convert it to a list
    if not isinstance(paths, list):
        paths = [paths]

    for path in paths:
        if not os.path.exists(path):
            continue

        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path, True)
