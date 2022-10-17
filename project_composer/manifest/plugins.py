from .base import BasePluginConfig
from .fields import CharField


class RequirementsConfig(BasePluginConfig):
    """
    Requirements file plugin.
    """
    _DEFAULT_INTRO = (
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.\n"
        "# Written on: {creation_date}\n\n"
    )
    _DEFAULT_CONTENT_FILENAME = "requirements.txt"
    _FIELDS = [
        CharField("application_label"),
        CharField("application_divider"),
        CharField("introduction", default=_DEFAULT_INTRO),
        CharField("source_filename", default=_DEFAULT_CONTENT_FILENAME),
        CharField("template"),
    ]
