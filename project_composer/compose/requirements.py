"""
=====================
Requirements composer
=====================

"""
from .text import TextContentComposer


class RequirementsComposer(TextContentComposer):
    _DEFAULT_CONTENT_FILENAME = "requirements.txt"
    _DEFAULT_APPLICATION_LABEL = "# {name}\n"
