# pylint: disable=redefined-outer-name

"""
A file that turns into an executable to
- generates a user definded latex template
- compiles latex document as well as clean residual files
"""
import argparse
import os
from commands import (
    clean_project,
    create_template,
    compile_pdf,
    rename_main,
    update_template,
)


def handle_argument(args) -> None:
    """
    Check the argument validity
    """
    if args.rename:
        rename_main(args.rename)
    elif args.clean:
        clean_project()
    elif args.template:
        create_template()
    elif args.update_template:
        update_template()

    if args.compile:
        # Checks argument is valid (.tex extension and existing file)
        target = args.compile
        if not target.endswith(".tex"):
            print("The file is not a LaTeX file")
            exit(-1)
        elif not os.path.isfile(target):
            print("The file does not exist")
            exit(-1)
        else:
            compile_pdf(target)
    exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--compile",
        type=str,
        help="Compiles a latex file into a pdf.",
        metavar=("TEX_FILE"),
    )
    parser.add_argument(
        "-r",
        "--rename",
        type=str,
        help="Update the name of the latex main file",
        metavar=("NEW_NAME"),
    )
    parser.add_argument(
        "-t",
        "--template",
        action="store_true",
        help="Creates a template from scratch.",
    )
    parser.add_argument(
        "-ut",
        "--update-template",
        action="store_true",
        help="Updates the previous template with the latest version.",
    )
    parser.add_argument(
        "-cl",
        "--clean",
        action="store_true",
        help=("Clean the project (template and main file)."),
    )

    args = parser.parse_args()
    handle_argument(args)
    print("No valid argument found.")
