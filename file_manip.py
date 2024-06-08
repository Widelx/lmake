"""
File manipulation utility
"""

import os
from unidecode import unidecode


def trim_ext(src: str) -> str:
    """
    Trim the extension of a given filename.
    """
    return os.path.splitext(src)[0]


def get_ext(src: str) -> str:
    """
    Return the extension of a given filename.
    """
    return os.path.splitext(src)[1]


def is_ext_type(src: str, ext: str):
    """
    Get indicator if the file is of the type ext.
    """
    return True if get_ext(src).lower() == ext.lower() else False


def update_ext(src: str, ext: str, apply: bool = False) -> str:
    """
    Update file extension for the given file path.
    Return the new file name.
    """
    src = src.removeprefix(os.sep)
    if apply and not os.path.isfile(src):
        raise FileNotFoundError(src)

    dirpath: str = os.path.dirname(src)
    file: str = os.path.basename(src)
    file = trim_ext(file) + ext
    dst: str = os.path.join(dirpath, file)

    if apply:
        os.rename(src, dst)
    return file


def normalize_name(src: str, apply: bool = False) -> str:
    """
    Normalize file/folder name for the given file/folder path.
    Return the new file name.
    """
    src: str = src.removeprefix(os.sep)
    if not os.path.isfile(src) and not os.path.isdir(src) and apply:
        raise FileNotFoundError(src)

    dirpath: str = os.path.dirname(src)
    file: str = os.path.basename(src).lower().replace(" ", "_")
    file = unidecode(file)
    dst: str = os.path.join(dirpath, file)

    if apply:
        os.rename(src, dst)
    return file
