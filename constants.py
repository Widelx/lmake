"""
A file containing constants
"""

# Edit the env variable name where all
# templates are available
TEMPLATE_ENV: str = "template"

# Shall not be edited
SETTINGS_FOLDER: str = ".vscode"
TEMPLATE_FOLDER: str = ".template"
MAIN_TEX: str = "main.tex"
ROOT_TEX: str = "% !TeX root ="

# Could be edited
FOLDER: str = "latex"
TEMPLATE_VERSION: str = "t_school_v1"
RE_TITLE_AUTHOR: str = (
    r"\\title{(?P<title>[\w\-_, ]*)}\n\\author{(?P<author>[\w\-_, ]*)}"
)
