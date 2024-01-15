# pylint: disable = unspecified-encoding

"""
A file generator for latex pdf.

This generator creates the pdf and
cleans the junk files
"""

import os
import re
import shutil
from constants import ROOT_TEX, RE_TITLE_AUTHOR, TEMPLATE_FOLDER


def get_sys_var(env_name: str) -> str:
    """
    Return the value of a system variable
    """
    return os.environ.get(env_name.upper())


def update_ext(file: str, extension: str = None) -> str:
    """
    Updates the file extension if a new one
    is provided. Else returns the raw
    name of the file (without extension)
    """
    if file is None:
        return None

    raw_file = os.path.splitext(file)[0]
    if extension:
        return raw_file + extension
    else:
        return raw_file


def clean_folders(files: list[str]) -> None:
    """
    Delete the specified folders.
    """
    for a_folder in files:
        if a_folder is not None:
            shutil.rmtree(a_folder, True)


def clean_files(files: list[str]) -> None:
    """
    Delete the specified files.
    """
    for a_file in files:
        if a_file is not None:
            try:
                os.remove(a_file)
            except OSError:
                pass


def customize_tplt(title: str, author: str) -> None:
    """
    Customize the template with the given title
    and author.
    """

    with open(f"{TEMPLATE_FOLDER}/title.tex", "r") as f:
        data: str = f.read()

    data: str = data.replace("ChangeTitle", title)
    data: str = data.replace("ChangeAuthor", author)

    with open(f"{TEMPLATE_FOLDER}/title.tex", "w") as f:
        f.write(data)


def parse_tplt() -> (str, str):
    """
    Customize the template with the given title
    and author.
    """

    with open(f"{TEMPLATE_FOLDER}/title.tex", "r") as f:
        data: str = f.read()

    matches: re.Match = re.search(RE_TITLE_AUTHOR, data)
    title: str = matches.group("title")
    author: str = matches.group("author")

    return (title, author)


def tag_file_as_root(f_name: str, old_name: str = "main.tex") -> None:
    """
    Make the "main" file the root folder.
    Without that latex workshop isn't able
    to compile.
    """
    with open(f_name, "r") as f:
        data = f.read()

    data = data.replace(
        f"{ROOT_TEX} {old_name}",
        f"{ROOT_TEX} {f_name}",
    )

    with open(f_name, "w") as f:
        f.write(data)


def find_main(dir_path: str) -> str:
    """
    Looks into the working folder
    and find a pattern that ids the
    "main.tex" file (root tex file).

    This function does not look for a name
    but instead for a pattern included by
    the template
    """
    files: list[str] = []
    main_file: str = None

    for a_file in os.listdir(dir_path):
        if a_file.endswith(".tex"):
            files.append(a_file)

    for a_tex_file in files:
        with open(a_tex_file, "r") as f:
            data = f.read()
            ret = data.find(ROOT_TEX)
            if ret != -1:
                main_file = a_tex_file
                break

    return main_file
