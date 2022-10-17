"""
Specific application exceptions.
"""


class ProjectComposerException(Exception):
    """
    Exception base.

    You should never use it directly except for test purpose. Instead make or
    use a dedicated exception related to the error context.
    """
    pass


class ComposerError(ProjectComposerException):
    """
    Error occuring from a ComposerBase class or inheriter.
    """
    pass


class ComposerConfigError(ProjectComposerException):
    """
    Error occuring from a BaseConfig class or inheriter.
    """
    pass


class ComposerManifestError(ProjectComposerException):
    """
    Error occuring from a manifest.
    """
    pass


class ComposerAppStoreError(ProjectComposerException):
    """
    Error occuring from Application store.
    """
    pass


class ComposerPurgeError(ProjectComposerException):
    """
    Error occuring when trying to purge an application repository.
    """
    pass
