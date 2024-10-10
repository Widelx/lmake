# pylint: disable=unspecified-encoding, line-too-long

import os
import re
import sys

from system import get_sys_var
from constants import (
    TEMPLATE_ENV_FOLDER,
    RE_TITLE_AUTHOR,
    ROOT_TEX,
    PROJ_TEMPLATE_FOLDER,
    TEMPLATE_SRC_FOLDER,
    TEMPLATE_TITLE_FILE,
)


def customize_tplt(title: str, author: str) -> None:
    """
    Customize the template with the given title and author.
    """
    (old_title, old_author) = parse_tplt()
    with open(
        os.path.join(
            os.getcwd(),
            PROJ_TEMPLATE_FOLDER,
            TEMPLATE_TITLE_FILE,
        ),
        "r+",
    ) as f:
        data: str = f.read()

        data = data.replace(old_title, title)
        data = data.replace(old_author, author)

        f.seek(0)
        f.truncate()
        f.write(data)


def parse_tplt() -> tuple[str, str]:
    """
    Parse the template with the title and author.
    """

    with open(f"{PROJ_TEMPLATE_FOLDER}/{TEMPLATE_TITLE_FILE}", "r") as f:
        data: str = f.read()

    match: re.Match = re.search(RE_TITLE_AUTHOR, data, re.MULTILINE)
    title: str = match.group("title")
    author: str = match.group("author")

    return (title, author)


def tag_file_as_root(f_name: str) -> None:
    """
    Make the "main" file the root folder.
    Without that, latex workshop isn't able to compile.
    """
    with open(f_name, "r") as f:
        lines: str = f.readlines()

    for index, line in enumerate(lines, 0):
        if line.find(ROOT_TEX) != -1:
            break

    lines[index] = f"{ROOT_TEX} {f_name}\n"

    with open(f_name, "w") as f:
        f.writelines(lines)


def is_main(file: str) -> bool:
    """
    Looks for the main file by searching for a specific tag.
    """
    file_path = os.path.join(os.getcwd(), file)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r+") as f:
        data = f.read()
        return True if data.find(ROOT_TEX) != -1 else False


def find_main(dirpath: str) -> str:
    """
    Look into the working folder and find a pattern that ids the "main.tex"
    file (root tex file).

    This function does not look for a name but instead for a pattern included
    by the template.
    """
    tex_files: list[str] = []
    main: str = None

    for file in os.listdir(dirpath):
        if file.endswith(".tex"):
            tex_files.append(file)

    for file in tex_files:
        if is_main(file):
            main = file
            break

    if main is None:
        raise FileNotFoundError(dirpath, " No latex main file was found.")

    return os.path.join(os.getcwd(), main)


def get_src_template_file(*args) -> str:
    """
    Return a path leading to a file or folder from source template.

    Throws an error if path does not exists.
    """
    src = os.path.join(
        get_sys_var(TEMPLATE_ENV_FOLDER), TEMPLATE_SRC_FOLDER, *list(args)
    )  # If using a dedicated latex folder for templates
    src_alt = os.path.join(
        get_sys_var(TEMPLATE_ENV_FOLDER), *list(args)
    )  # If not using a dedicated latex folder for templates

    if os.path.exists(src):
        return src
    elif os.path.exists(src_alt):
        return src_alt
    else:
        print("[ERROR] Template folder not found.")
        sys.exit(-1)
