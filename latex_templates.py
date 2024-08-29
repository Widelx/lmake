#pylint: disable = missing-module-docstring

from string import Template

TITLE_TEMPLATE = Template("""\\subsection*{$title}""")

IMAGE_TEMPLATE = Template(
    """\\image[0.5]
{$path}
{Ajoutez une description}"""
)
