"""
========
Manifest
========

"""
import json
from pathlib import Path

import tomli

from .exceptions import ComposerManifestError


class BaseConfig:
    """
    Configuration class abstract.

    Attributes:
        _FIELDS (list): List of payload attribute names. Only those attributes will
            be available to dump.
    """
    _FIELDS = []

    def get_fields(self):
        """
        Return model payload attribute names.

        Returns:
            list: List name string for each payload attribute.
        """
        return self._FIELDS

    def to_dict(self):
        """
        Dump manifest values as Python dictionnary.

        Recursively walk in ``to_dict`` method of item that are a children of
        BaseConfig.

        Returns:
            dict: Dictionnary of all field values, including the "requirements"
            ones.
        """
        content = {}

        for name in self.get_fields():
            attr = getattr(self, name)
            if isinstance(attr, BaseConfig):
                content[name] = attr.to_dict()
            else:
                content[name] = getattr(self, name)

        return content


class TextContentConfig(BaseConfig):
    """
    Configuration class for TextContent alike plugin.
    """
    _FIELDS = [
        "application_label",
        "application_divider",
        "introduction",
        "source_filename",
        "template",
    ]
    _DEFAULT_INTRO = (
        "# This file is automatically overwritten by composer, DO NOT EDIT IT.\n"
        "# Written on: {creation_date}\n\n"
    )
    _DEFAULT_CONTENT_FILENAME = "source.txt"

    def __init__(self, application_label=None, application_divider=None, template=None,
                 introduction=None, source_filename=None):
        # TODO: Attributes should be set from _FIELDS
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
    Requirements file plugin.
    """
    _DEFAULT_CONTENT_FILENAME = "requirements.txt"


class Manifest(BaseConfig):
    """
    Manifest model.

    NOTE: Currently adding new fields will need some declarations changes here and
    there because there is not strong declaration yet as in real data model.

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
        requirements (dict or RequirementsConfig): Requirements specific options.
            Either as RequirementsConfig object or a dict of values respecting the
            RequirementsConfig attributes.
    """
    # Payload fields declaration
    _FIELDS = [
        "name",
        "apps",
        "repository",
        "syspaths",
        "requirements",
    ]

    def __init__(self, name, apps, repository=None, syspaths=None, requirements=None):
        self.name = name
        self.apps = apps
        self.repository = repository
        self.syspaths = syspaths or []

        # For possible future new parts, we would need about a plugins namespace where
        # to register 'requirements' and other parts as a plugin.
        _reqs = requirements or {}
        if isinstance(_reqs, RequirementsConfig):
            self.requirements = _reqs
        else:
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

            # JSON format is the simpliest structure which fit exactly to the manifest
            # structure
            if source.name.endswith(".json"):
                content = json.loads(source.read_text())
            # TOML format is more complex than manifest structure
            elif source.name.endswith(".toml"):
                loaded = tomli.loads(source.read_text())

                # Check required structure
                if (
                    "tool" not in loaded or
                    "project_composer" not in loaded["tool"]
                ):
                    raise ComposerManifestError(
                        "TOML manifest must have a section [tool.project_composer] to "
                        "fill base options."
                    )

                composer_section = loaded["tool"]["project_composer"]

                # Build payload
                content = {
                    name: composer_section.get(name, None)
                    for name in cls._FIELDS
                }

                # If there is no composer config name, try to use the TOML project one
                if not content["name"]:
                    content["name"] = loaded.get("project", {}).get("name", "")

            # No recognized format
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
