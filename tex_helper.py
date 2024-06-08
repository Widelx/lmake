# pylint: disable=unspecified-encoding

import os
import re

from constants import (
    RE_TITLE_AUTHOR,
    ROOT_TEX,
    PROJ_TEMPLATE_FOLDER,
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

    match: re.Match = re.search(RE_TITLE_AUTHOR, data)
    title: str = match.group("title")
    author: str = match.group("author")

    return (title, author)


def tag_file_as_root(f_name: str, old_name: str = "main.tex") -> None:
    """
    Make the "main" file the root folder.
    Without that, latex workshop isn't able to compile.
    """
    with open(f_name, "r+") as f:
        data: str = f.read()
        data = data.replace(f"{ROOT_TEX} {old_name}", f"{ROOT_TEX} {f_name}")

        f.seek(0)
        f.truncate()
        f.write(data)


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
