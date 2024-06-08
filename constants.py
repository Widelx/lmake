"""
Project constants
"""

TEMPLATE_SYS_ENV: str = "template"
TEMPLATE_NAME: str = "t_school_v1"
TEMPLATE_SRC_FOLDER: str = "latex"

# Folders name
PROJ_TEMPLATE_FOLDER: str = ".template"
PROJ_SETTINGS_FOLDER: str = ".vscode"

BUILD_FOLDER: str = "temp"

TEMPLATE_TITLE_FILE: str = "title.tex"
MAIN_TEX: str = "main.tex"
ROOT_TEX: str = "% !TeX root ="

RE_TITLE_AUTHOR: str = (
    r"\\title{(?P<title>[\w\-_, ]*)}\n\\author{(?P<author>[\w\-_, ]*)}"
)
