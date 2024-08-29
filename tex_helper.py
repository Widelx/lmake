# pylint: disable=unspecified-encoding, line-too-long

import os
import re
import sys

from system import get_sys_var
from data import TemplateData
from constants import (
    TEMPLATE_ENV_FOLDER,
    ROOT_TEX,
    PROJ_TEMPLATE_FOLDER,
    TEMPLATE_CUSTOMIZATION_FILE,
    TEMPLATE_SRC_FOLDER,
    RE_AUTHOR,
    RE_C_FOOTER,
    RE_L_FOOTER,
    RE_R_FOOTER,
    RE_TITLE,
)


def customize_tplt() -> None:
    """
    Customize the template with user inputs.
    """
    t_data: TemplateData = TemplateData()

    f_path = os.path.join(
        os.getcwd(), PROJ_TEMPLATE_FOLDER, TEMPLATE_CUSTOMIZATION_FILE
    )
    with open(f_path, "r") as f:
        data: str = f.read()

    m: re.Match = re.search(RE_TITLE, data)
    old_title = m.group(1)
    m = re.search(RE_AUTHOR, data)
    old_authors = m.group(1)
    m = re.search(RE_L_FOOTER, data)
    old_l_footer = m.group(1)
    m = re.search(RE_C_FOOTER, data)
    old_c_footer = m.group(1)
    m = re.search(RE_R_FOOTER, data)
    old_r_footer = m.group(1)

    data = data.replace(old_title, t_data.title)
    data = data.replace(old_authors, t_data.authors)
    data = data.replace(old_l_footer, t_data.l_footer)
    data = data.replace(old_c_footer, t_data.c_footer)
    data = data.replace(old_r_footer, t_data.r_footer)

    with open(f_path, "w") as f:
        f.write(data)


def parse_tplt() -> None:
    """
    Parse the template with the title and author.
    """
    t_data = TemplateData()

    with open(f"{PROJ_TEMPLATE_FOLDER}/{TEMPLATE_CUSTOMIZATION_FILE}", "r") as f:
        data: str = f.read()

    m: re.Match = re.search(RE_TITLE, data)
    t_data.title = m.group(1)
    m = re.search(RE_AUTHOR, data)
    t_data.authors = m.group(1)
    m = re.search(RE_L_FOOTER, data)
    t_data.l_footer = m.group(1)
    m = re.search(RE_C_FOOTER, data)
    t_data.c_footer = m.group(1)
    m = re.search(RE_R_FOOTER, data)
    t_data.r_footer = m.group(1)


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
