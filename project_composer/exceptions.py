"""
Exceptions
==========

Specific application exceptions.
"""


class ProjectComposerException(Exception):
    """
    Exception base.

    You should never use it directly except for test purpose. Instead make or
    use a dedicated exception related to the error context.
    """
    pass


class ComposerManifestError(ProjectComposerException):
    """
    Error occuring when loading manifest.
    """
    pass
