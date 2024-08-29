"""
Dataclasses
"""

from dataclasses import dataclass

class Singleton(type):
    """
    Singleton implementation in python
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

@dataclass()
class TemplateData(metaclass=Singleton):
    """
    Store custom template properties
    """
    fname: str = ""
    title: str = ""
    authors: str = ""
    l_footer: str = ""
    c_footer: str = ""
    r_footer: str = ""