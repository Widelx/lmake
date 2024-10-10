"""
Top level commands called by the script
"""

# pylint: disable=invalid-name, wildcard-import, unused-wildcard-import, bare-except

import os
import shutil

from system import *
from file_manip import normalize_name, update_ext
from constants import (
    BUILD_FOLDER,
    MAIN_TEX,
    PROJ_TEMPLATE_FOLDER,
    TEMPLATE_NAME,
    PROJ_SETTINGS_FOLDER,
)
from tex_helper import (
    customize_tplt,
    find_main,
    get_src_template_file,
    is_main,
    parse_tplt,
    tag_file_as_root,
)


def compile_tex(target: str = None) -> None:
    """
    Generate a pdf file from a latex main file and its dependencies.

    1 - Clean the folder (in case the previous call was a fail).
    2 - Calls texlive pdf generator using a shell command.
    3 - Verifies the generation status.
    4 - Cleans the build folder is successful.
    """
    if target is None:
        target = find_main(os.getcwd())

    if not is_main(target):
        raise TypeError(target, " is not a root tex file")

    pdf_result: str = update_ext(target, ".pdf")

    # Cleans the previous files
    remove_f([pdf_result, BUILD_FOLDER])

    os.mkdir(BUILD_FOLDER)
    cmd = os.popen(
        f"pdflatex -shell-escape -output-directory={BUILD_FOLDER} -interaction=batchmode {target}"
    )
    cmd.readlines()
    success = cmd.close()

    if success:
        shutil.copy2(os.path.join(BUILD_FOLDER, pdf_result), os.getcwd())
        remove_f(BUILD_FOLDER)
        print(f'PDF "{pdf_result}" generated.')

    else:
        print("[ERROR] Generation failed. Please check the logs")
        exit(-1)


def create_template() -> None:
    """
    Generates a custom template in the directory.

    The generated template is issued from a copy stored elsewhere which is then edited with
    the following parameter:
    - name main tex file.
    - title.
    - author[s].
    """
    # fmt: off
    print              ("Template creation")
    print              ("**********")
    f_name: str = input("File name:")
    title : str = input("Title    :")
    author: str = input("Author   :")
    print              ("**********")
    # fmt: on

    # Copy latex template in the current directory
    template_src: str = get_src_template_file(TEMPLATE_NAME)

    shutil.copytree(template_src, os.getcwd(), dirs_exist_ok=True)

    # Copy vscode settings in the current directory
    settings_src: str = get_src_template_file(PROJ_SETTINGS_FOLDER)
    settings_dest: str = os.path.join(os.getcwd(), PROJ_SETTINGS_FOLDER)
    shutil.copytree(settings_src, settings_dest, dirs_exist_ok=True)

    # Update template
    customize_tplt(title, author)

    if f_name:
        rename_main(f_name)


def reload_template() -> None:
    """
    Reload an existing template with the latest version available.
    """
    (title, author) = parse_tplt()

    # Copy the template in the current directory
    src: str = get_src_template_file(TEMPLATE_NAME, PROJ_TEMPLATE_FOLDER)
    dst: str = os.path.join(os.getcwd(), PROJ_TEMPLATE_FOLDER)
    shutil.copytree(src, dst, dirs_exist_ok=True)

    customize_tplt(title, author)


def rename_main(new: str = MAIN_TEX) -> None:
    """
    Rename the main file.
    """
    old: str = find_main(os.getcwd())

    os.rename(old, new)
    new = update_ext(new, ".tex", apply=True)
    new = normalize_name(new, apply=True)

    tag_file_as_root(new)

    # Update the pdf as well
    remove_f(update_ext(old, ".pdf"))
    compile_tex(new)


def clean_project() -> None:
    """
    Clean the project in the working dir:
    - removes the main tex file.
    - removes the template tree.
    """
    main_file: str = find_main(os.getcwd())
    remove_f(
        [
            main_file,
            update_ext(main_file, ".pdf"),
            PROJ_TEMPLATE_FOLDER,
            PROJ_SETTINGS_FOLDER,
            BUILD_FOLDER,
        ]
    )
