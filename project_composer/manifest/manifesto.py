import json
from pathlib import Path

import tomli

from ..exceptions import ComposerManifestError

from .base import BaseConfig
from .fields import CharField, ListField, PluginField, BooleanField
from .plugins import RequirementsConfig


class Manifest(BaseConfig):
    """
    The manifest model.

    Manifest fields are given as keyword arguments.

    Fields are:

    name (string)
        The manifest title name.

    collection (list)
        A list of application module names for enabled application.
    repository (string)
        A Python path where to search for enabled application
        modules.
    syspaths (list)
        A list of Path object to load in sys.path by Composer.
    requirements (dict)
        A dictionnary of items to load in ``RequirementsConfig``
        for specific requirements composer. In fact this is used by
        ``TextContentComposer`` but requirements is actually its unique
        implementation.

    Attributes:
        name (string): The manifest title name.
        collection (list): A list of application module names for enabled application.
        requirements (dict or RequirementsConfig): Requirements specific options.
            Either as RequirementsConfig object or a dict of values respecting the
            RequirementsConfig attributes.
    """
    # Payload fields declaration
    _FIELDS = [
        CharField("name", required=True),
        ListField("collection", required=True),
        CharField("repository", required=True),
        CharField("default_store_app"),
        BooleanField("no_ordering"),
        ListField("syspaths"),
        PluginField("requirements", plugin=RequirementsConfig),
    ]

    @classmethod
    def load(cls, source):
        """
        Loading a manifest source.

        Arguments:
            cls (class): Manifest class.
            source (string or pathlib.Path or dict or Manifest): The Manifest source to
                load. It can be either:

                * A Manifest object, it will just be returned as it without any
                  validation, you are responsible of its correctness;
                * A string for the file path to load in JSON or TOML format;
                * A Path object to the file to load in JSON or TOML format;
                * A Dictionnary which respect the manifest structure;

                Source file format are guessed from their file extension such as JSON
                for ``.json`` or TOML for ``.toml``.

        Return:
            Manifest: A Manifest model instance.
        """
        if isinstance(source, cls):
            # That should commonly not happen but if a Manifest object is given, just
            # use it directly and bypass everything else.
            return source
        elif isinstance(source, dict):
            # A dict is directly used as content
            content = source
        else:
            # Enforce Path object
            source = Path(source)

            # JSON format is the simpliest structure which fit exactly to the manifest
            # structure
            if source.name.endswith(".json"):
                content = json.loads(source.read_text())
            # TOML format is more complex than manifest structure and need to be
            # built correctly
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

                content = loaded["tool"]["project_composer"]

                # If there is no composer config name, try to use the TOML project one
                if not content.get("name"):
                    pyproject_name = loaded.get("project", {}).get("name")
                    if pyproject_name:
                        content["name"] = pyproject_name

            # No recognized format
            else:
                raise ComposerManifestError(
                    "Unable to guess the manifest file format. Please suffix your "
                    "filename either with '.json' or '.toml' depending it is a JSON "
                    "or a TOML format."
                )

        # Build Manitest keyword arguments from retrieved content, only retains items
        # knowed as manifest fields
        kwargs = {
            k: v
            for k, v in content.items()
            if k in cls.get_fieldnames()
        }

        return cls(**kwargs)
