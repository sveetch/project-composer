"""
=============
Base composer
=============

"""
import json
import sys
import inspect

from ..exceptions import ComposerManifestError
from ..importer import import_module
from ..logger import LoggerBase


class ComposerBase(LoggerBase):
    """
    Composer base implements everything about application module discovering and
    manifest loading.

    Arguments:
        manifest_path (pathlib.Path or dict): Either a path to the manifest file to load
            or directly the manifest dictionnary.
        appsdir_pythonpath (string): Python path where to search for application
            modules.

    Keyword Arguments:
        base_syspaths (list): A list of path to insert in sys.path, this is required if
            ``appsdir_pythonpath`` is not available directly in the current working
            directory. You are responsible to no set twice paths, erroneous paths, etc..
            There is no validation for the paths you give.

    Attributes:
        _MODULE_PYTHONPATH (string): A template string to build the full Python path
            of founded class. It expected two variable ``parent`` and ``name``,
            respectively the module path and the class name.
    """
    _MODULE_PYTHONPATH = "{parent}.{name}"

    def __init__(self, manifest_path, appsdir_pythonpath, **kwargs):
        self.base_syspaths = None
        if "base_syspaths" in kwargs:
            self.base_syspaths = kwargs.pop("base_syspaths")

        self.manifest_path = manifest_path
        self.appsdir_pythonpath = appsdir_pythonpath

        super().__init__()

        self.manifest = self.get_manifest(self.manifest_path)
        self.apps = self.manifest["apps"]

        for item in (self.base_syspaths or []):
            sys.path.append(item)

    def get_module_path(self, name):
        """
        Return a Python path for a module name.

        Arguments:
            name (string): Module name.

        Returns:
            string: Module name prefixed with ``ComposerBase.appsdir_pythonpath`` if
            it is not empty else returns just the module name.
        """
        if self.appsdir_pythonpath:
            return self._MODULE_PYTHONPATH.format(
                parent=self.appsdir_pythonpath,
                name=name,
            )

        return name

    def get_manifest(self, path):
        """
        Load manifest from JSON file, validate it and return it as Python object.

        Arguments:
            path (pathlib.Path or dict): Either a path to the manifest file to load
                or directly the manifest dictionnary.

        Returns:
            dict: The manifest.
        """
        if isinstance(path, dict):
            content = path
        else:
            content = json.loads(path.read_text())

        if not isinstance(content, dict):
            raise ComposerManifestError("Manifest content should be a dictionnary.")

        if "apps" not in content:
            raise ComposerManifestError("Manifest require an item 'apps'.")

        return content

    def find_app_module(self, name):
        """
        Find a module (by its pythonpath) from application.

        Arguments:
            name (string): Module pythonpath.

        Returns:
            object: Module object if found else None.
        """
        try:
            module = import_module(name)
        except ModuleNotFoundError:
            self.log.warning("Unable to find module: {}".format(name))
            return None
        else:
            return module

    def _is_elligible_class(self, obj):
        """
        Find if given object is an enabled class for composition.

        Criterias for eligibility are in order:

        * Object is a class;
        * Object is not named ``EnabledApplicationMarker``;
        * Object got attribute ``_ENABLED_COMPOSABLE_APPLICATION`` which value is not
          ``None``;

        Arguments:
            obj (object): Object to check for eligibility.

        Returns:
            boolean: ``True`` if object is eligibile to criterias else ``False``.
        """
        if (
            inspect.isclass(obj) and
            getattr(obj, "__name__", None) != "EnabledApplicationMarker" and
            getattr(obj, "_ENABLED_COMPOSABLE_APPLICATION", None) is not None
        ):
            return True

        return False

    def _get_elligible_module_classes(self, path, module):
        """
        Get all elligible classes from a module.

        Arguments:
            path (string): The Python path to a module, only used in logging messages.
            module (object): The module object where to find elligible classes.

        Returns:
            list: List of elligible classes objects.
        """
        enabled = []

        if not hasattr(module, "__dict__"):
            raise NotImplementedError("Module object must have a '__dict__' attribute.")

        for object_name in module.__dict__.keys():
            if not object_name.startswith("_"):
                obj = getattr(module, object_name)
                if self._is_elligible_class(obj):
                    self.log.debug("Got enabled class at: {}.{}".format(
                        path,
                        object_name,
                    ))
                    if obj not in enabled:
                        enabled.append(obj)

        return enabled
