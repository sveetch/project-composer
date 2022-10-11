"""
========
Manifest
========

"""
import json
from pathlib import Path

import tomli

from .exceptions import ComposerManifestError


class TextContentConfig:
    """
    Dedicated manifest part model to TextContent operations.
    """
    _FIELDS = [
        "application_label",
        "application_divider",
        "dump",
        "introduction",
        "source_filename",
        "template",
    ]
    _DEFAULT_INTRO = (
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.\n"
        "# Written on: {creation_date}\n\n"
    )
    _DEFAULT_CONTENT_FILENAME = "source.txt"

    def __init__(self, dump=None, minimal=False, application_label=None,
                 application_divider=None, template=None, introduction=None,
                 source_filename=None):
        self.dump = dump
        self.application_label = application_label
        self.application_divider = application_divider
        self.template = template
        self.source_filename = source_filename or self._DEFAULT_CONTENT_FILENAME

        if introduction is False:
            self.introduction = None
        elif introduction is None:
            self.introduction = self._DEFAULT_INTRO
        else:
            self.introduction = introduction


class RequirementsConfig(TextContentConfig):
    """
    Requirements class so options are reachable as proper object attributes in their
    own namespace
    """
    _DEFAULT_CONTENT_FILENAME = "requirements.txt"


class Manifest:
    """
    Manifest model.

    Arguments:
        name (string): The manifest title name.
        apps (list): A list of application module names for enabled application.

    Keyword Arguments:
        repository (string): A Python path where to search for enabled application
            modules.
        syspaths (list): A list of Path object to load in sys.path by Composer.
        requirements (dict): A dictionnary of items to load in ``RequirementsConfig``
            for specific requirements composer. In fact this is used by
            ``TextContentComposer`` but requirements is actually its unique
            implementation.

    Attributes:
        name (string): The manifest title name.
        apps (list): A list of application module names for enabled application.
        requirements (RequirementsConfig): Requirements specific options.
    """
    def __init__(self, name, apps, repository=None, syspaths=None, requirements=None):
        self.name = name
        self.apps = apps
        self.repository = repository
        self.syspaths = syspaths or []

        # For possible future new parts, we would need about a plugins namespace where
        # to register 'requirements' and other parts as a plugin.
        _reqs = requirements or {}
        self.requirements = RequirementsConfig(**_reqs)

        super().__init__()

    @classmethod
    def validate(cls, name, apps, repository=None, syspaths=None, requirements=None):
        """
        Validate a manifest object.
        """
        if apps is None or not isinstance(apps, list):
            raise ComposerManifestError(
                "Manifest 'apps' option is a required item and must be a list."
            )

    @classmethod
    def load(cls, source):
        """
        Loading a manifest source.

        Arguments:
            cls (class): Manifest class.
            source (string or pathlib.Path or dict or Manifest): The Manifest source to
                load. It can be either:

                * A Manifest object, it will just returned as it without any validation,
                  you are responsible of its correctness;
                * A string for the file path to load in JSON or TOML format;
                * A Path object to the file to load in JSON or TOML format;
                * A Dictionnary which respect the manifest structure;

                Source file format are guessed from their file extension such as JSON
                for ``.json`` or TOML for ``.toml``.

        Return:
            Manifest: A Manifest model instance.
        """
        if isinstance(source, cls):
            return source
        elif isinstance(source, dict):
            content = {
                "name": source.get("name", ""),
                "apps": source.get("apps", None),
                "repository": source.get("repository", None),
                "syspaths": source.get("syspaths", None),
                "requirements": source.get("requirements", None),
            }
        else:
            # Enforce Path object
            source = Path(source)

            if source.name.endswith(".json"):
                content = json.loads(source.read_text())
            elif source.name.endswith(".toml"):
                loaded = tomli.loads(source.read_text())

                if (
                    "tool" not in loaded or
                    "project_composer" not in loaded["tool"]
                ):
                    raise ComposerManifestError(
                        "TOML manifest must have a section [tool.project_composer] to "
                        "fill base options."
                    )

                content = {
                    "name": loaded.get("project", {}).get("name", ""),
                    "apps": loaded["tool"]["project_composer"].get("apps", None),
                    "requirements": loaded["tool"]["project_composer"].get(
                        "requirements"
                    ),
                }
            else:
                raise ComposerManifestError(
                    "Unable to guess the manifest file format. Please suffix your "
                    "filename either with '.json' or '.toml' depending it is a JSON "
                    "or a TOML format."
                )

        name = content.get("name", "")
        apps = content.get("apps", None)
        repository = content.get("repository", None)
        syspaths = content.get("syspaths", None)
        requirements = content.get("requirements", {})

        cls.validate(name, apps, repository=repository, syspaths=syspaths,
                     requirements=requirements)

        return cls(name, apps, repository=repository, syspaths=syspaths,
                   requirements=requirements)
