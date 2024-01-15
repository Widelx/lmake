"""
Top level commands
"""

# pylint: disable=invalid-name, wildcard-import, unused-wildcard-import, bare-except

import os
import shutil
import sys
from unidecode import unidecode

from constants import (
    MAIN_TEX,
    TEMPLATE_ENV,
    FOLDER,
    TEMPLATE_FOLDER,
    TEMPLATE_VERSION,
    SETTINGS_FOLDER,
)
from helper import *


def compile_pdf(target: str) -> None:
    """
    Generates a pdf file from a latex main file and its dependencies.

    1 - Cleans the folder (in case the previous call was a fail)
    2 - Calls texlive pdf generator using a shell command
    3 - Verifies the generation status
    4 - Cleans the junk files that were created.
    """
    pdf_result: str = update_ext(target, ".pdf")
    raw_file_name: str = update_ext(target)

    # Cleans the previous files (if doable)
    clean_files([pdf_result])
    clean_folders(["temp"])

    os.mkdir("temp")
    cmd = os.popen(
        f"pdflatex -shell-escape -output-directory=temp -interaction=batchmode {target}"
    )
    cmd.readlines()
    status = cmd.close()

    if not status:
        # Generation failed
        clean_folders([f"_minted-{raw_file_name}"])
        print("[ERROR] Generation failed. Please check the logs")
        exit(-1)

    else:
        # Generation success
        shutil.copy2(f"temp/{pdf_result}", os.getcwd())
        clean_folders(["temp", f"_minted-{raw_file_name}"])
        print(f'PDF "{pdf_result}" generated.')


def create_template() -> None:
    """
    Generates a custom template in the directory.

    The generated template is issued from a copy
    stored elsewhere which is then edited with
    the following parameter:
    - name main tex file
    - title
    - author[s]
    """
    # fmt: off
    print              ("Template creation")
    print              ("*****************")
    f_name: str = input("File name: "      )
    title : str = input("Title    : "      )
    author: str = input("Author   : "      )
    print              ("*****************")
    # fmt: on

    # Copies the template in the current directory
    template_src: str = f"{get_sys_var(TEMPLATE_ENV)}\\{FOLDER}\\{TEMPLATE_VERSION}"
    shutil.copytree(template_src, os.getcwd(), dirs_exist_ok=True)

    # Copies the settings in the current directory
    settings_src: str = f"{get_sys_var(TEMPLATE_ENV)}\\{FOLDER}\\{SETTINGS_FOLDER}"
    settings_dest: str = f"{os.getcwd()}\\{SETTINGS_FOLDER}"
    shutil.copytree(settings_src, settings_dest, dirs_exist_ok=True)

    # Updates the template
    customize_tplt(title, author)

    if f_name:
        rename_main(f_name, MAIN_TEX)

    print("Template created")


def update_template() -> None:
    """
    Updates an existing template with the latest
    version available
    """
    title, author = parse_tplt()

    # Copies the template in the current directory
    template_src: str = (
        f"{get_sys_var(TEMPLATE_ENV)}\\{FOLDER}\\{TEMPLATE_VERSION}\\{TEMPLATE_FOLDER}"
    )
    template_dest: str = f"{os.getcwd()}\\{TEMPLATE_FOLDER}"
    shutil.copytree(template_src, template_dest, dirs_exist_ok=True)

    customize_tplt(title, author)


def rename_main(new: str, old: str = None) -> None:
    """
    Rename the main file
    """
    # No spaces allowed
    new = new.replace(" ", "_")

    if not old:
        DIR_PATH: str = os.getcwd()
        main_file: str = find_main(DIR_PATH)

        if not main_file:
            print("[ERROR] Main file was not found. Renaming aborted.")
            sys.exit(-1)

        old: str = main_file.removeprefix(DIR_PATH)

    new: str = update_ext(new, ".tex")
    new = unidecode(new)
    os.rename(old, new)
    tag_file_as_root(new, old)

    # Clean the previous generated pdf
    clean_files([update_ext(old, ".pdf")])


def clean_project() -> None:
    """
    Clean the project in the working dir:
    - removes the main tex file
    - removes the template tree
    """
    DIR_PATH: str = os.getcwd()
    main_file: str = find_main(DIR_PATH)
    clean_files([main_file, update_ext(main_file, ".pdf")])
    clean_folders([TEMPLATE_FOLDER, SETTINGS_FOLDER])
