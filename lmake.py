# pylint: disable=redefined-outer-name

"""
Root executable with helper
"""

import argparse
import sys
from commands import (
    clean_project,
    create_template,
    compile_tex,
    edit_template,
    rename_main,
    reload_template,
)
from file_manip import is_ext_type


def handle_argument(args) -> None:
    """
    Call the functions associated to the given argument.
    """
    if args.rename:
        rename_main(args.rename)

    if args.clean:
        print("Are you sure that you want to delete everything ? (Y/N) :", end="")
        if input().lower() == "y":
            clean_project()
        else:
            sys.exit(-1)

    if args.template:
        create_template()

    if args.reload_template:
        reload_template()

    if args.edit_template:
        edit_template()

    if args.compile:
        compile_tex(None if args.compile is True else args.compile)


def is_tex_file(target: str):
    """
    Check wether the target is a latex file.

    This function does not check empty target (tagged as true).
    """
    if target is True or is_ext_type(target, ".tex"):
        return target
    else:
        raise argparse.ArgumentTypeError("File must be a tex file.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="tool",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50),
    )
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-c",
        "--compile",
        type=is_tex_file,
        action="store",
        const=True,
        nargs="?",
        help="Compiles a latex file into a pdf.",
        metavar=("TEX_FILE"),
    )
    group.add_argument(
        "-r",
        "--rename",
        type=str,
        action="store",
        help="Update name of latex main file",
        metavar=("NEW_NAME"),
    )
    group.add_argument(
        "-t",
        "--template",
        action="store_true",
        help="Creates a template from scratch.",
    )
    group.add_argument(
        "-rt",
        "--reload-template",
        action="store_true",
        help="Reload previous template with the latest version.",
    )
    group.add_argument(
        "-et",
        "--edit-template",
        action="store_true",
        help="Edit attributes of an existing template.",
    )
    group.add_argument(
        "-cl",
        "--clean",
        action="store_true",
        help=("Clean project (template as well as main file)."),
    )

    args = parser.parse_args()
    handle_argument(args)
