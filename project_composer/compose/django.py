"""
=====================
Django parts composer
=====================

"""
from .classes import ClassComposer


class ComposeDjangoSettings(ClassComposer):
    """
    Composer for enabled application settings classes for a Django project.
    """
    _MODULE_PYTHONPATH = "{parent}.{name}.settings"


class ComposeDjangoUrls(ClassComposer):
    """
    Composer for enabled application urls classes for a Django project.
    """
    _MODULE_PYTHONPATH = "{parent}.{name}.urls"
