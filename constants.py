"""
Project constants
"""

TEMPLATE_ENV_FOLDER: str = "template"
TEMPLATE_NAME: str = "t_school_v1"
TEMPLATE_SRC_FOLDER: str = "latex"

# Folders name
PROJ_TEMPLATE_FOLDER: str = ".template"
PROJ_SETTINGS_FOLDER: str = ".vscode"

BUILD_FOLDER: str = "temp"

TEMPLATE_CUSTOMIZATION_FILE: str = "doc_data.tex"
MAIN_TEX: str = "main.tex"
ROOT_TEX: str = "% !TeX root ="

RE_TITLE: str = r"\\title{(.*)}\n"
RE_AUTHOR: str = r"\\author{(.*)}\n"
RE_L_FOOTER: str = r"\\fancyfoot\[L\]{(.*)}\n"
RE_C_FOOTER: str = r"\\fancyfoot\[C\]{(.*)}\n"
RE_R_FOOTER: str = r"\\fancyfoot\[R\]{(.*)}\n"
