import sys
import inspect

from .app_storage import AppStore
from .exceptions import ComposerError
from .importer import import_module
from .logger import LoggerBase
from .manifest import Manifest


class Composer(LoggerBase):
    """
    Composer base implements everything about application module discovering and
    manifest loading.

    Arguments:
        manifest (string or pathlib.Path or dict or Manifest): The Manifest source to
            load. It can be either:

            * A Manifest object, it will just returned as it without any validation,
                you are responsible of its correctness;
            * A string for the file path to load in JSON or TOML format;
            * A Path object to the file to load in JSON or TOML format;
            * A Dictionnary which respect the manifest structure;

            Source file format are guessed from their file extension such as JSON
            for ``.json`` or TOML for ``.toml``.
        processors (list): List of available composition processors classes.

    Attributes:
        _APPLICATION_MODULE_PYTHONPATH (string): A template string to build the full
            Python path of founded class. It expected two variable ``parent`` and
            ``name``, respectively the module path and the class name.
    """
    _APPLICATION_MODULE_PYTHONPATH = "{parent}.{name}"

    def __init__(self, manifest, processors=[]):
        super().__init__()

        self.manifest = self.get_manifest(manifest)
        self.set_syspaths(self.manifest.syspaths or [])

        self.store = AppStore(default_app=self.manifest.default_store_app)

        self.apps = []

        # Register and initialize all given processors
        self.processors = {
            proc.__name__: proc(self)
            for proc in processors
        }

    def call_processor(self, name, method, **kwargs):
        """
        Return loaded manifest object.

        Arguments:
            name (string): Processor name in registry.
            method (string): Processor method to execute.
            **kwargs: Keyword arguments to pass to method if any.

        Returns:
            object: Content depend from Processor method returns.
        """
        if name not in self.processors:
            msg = "Given processor name is not registered from composer: {}"
            raise ComposerError(msg.format(name))

        if not hasattr(self.processors[name], method):
            msg = "Processor '{proc}' don't have any method named '{method}'"
            raise ComposerError(msg.format(proc=name, method=method))

        return getattr(self.processors[name], method)(**kwargs)

    def get_manifest(self, manifest):
        """
        Return loaded manifest object.

        Arguments:
            manifest (string or pathlib.Path or dict or Manifest): The Manifest source
                to load.

        Returns:
            Manifest: The manifest object loaded from given source.
        """
        return Manifest.load(manifest)

    def set_syspaths(self, paths):
        """
        Append each item path to ``sys.path``.

        This won't never append a same path twice.

        Arguments:
            paths (list): A list of path to append.
        """
        for path in paths:
            if path not in sys.path:
                sys.path.append(path)

    def get_application_base_module_path(self, name):
        """
        Return the Python path to the application base module.

        Commonly this should be the ``__init__.py`` file from application directory.

        Arguments:
            name (string): Module name.

        Returns:
            string: Module name prefixed with repository path if it is not empty else
            returns just the module name.
        """
        if self.manifest.repository:
            return self._APPLICATION_MODULE_PYTHONPATH.format(
                parent=self.manifest.repository,
                name=name,
            )

        return name

    def get_module_path(self, name):
        """
        Return a Python path for a module name.

        Arguments:
            name (string): Module name.

        Returns:
            string: Module name prefixed with repository path if it is not empty else
            returns just the module name.
        """
        return self.get_application_base_module_path(name)

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
            msg = "{klass} is unable to find module: {path}".format(
                klass=self.__class__.__name__,
                path=name,
            )
            self.log.warning(msg)
            return None
        else:
            return module

    def _is_elligible_class(self, obj):
        """
        Find if given object is an enabled class for composition.

        Criterias for eligibility are in order:

        * Object is a class;
        * Class is not named ``EnabledApplicationMarker``;
        * Class got attribute ``_ENABLED_COMPOSABLE_APPLICATION`` which value is not
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
            path (string): The Python path to a module used for reporting and logging
                messages.
            module (object): The module object where to find elligible classes.

        Returns:
            list: List of elligible classes objects.
        """
        enabled = []

        if not hasattr(module, "__dict__"):
            msg = "Module object from '{}' must have a '__dict__' attribute."
            raise ComposerError(msg.format(path))

        for object_name in module.__dict__.keys():
            if not object_name.startswith("_"):
                obj = getattr(module, object_name)

                if self._is_elligible_class(obj):
                    msg = "{klass} found enabled Class at: {path}.{object_name}".format(
                        klass=self.__class__.__name__,
                        path=path,
                        object_name=object_name,
                    )
                    self.log.debug(msg)

                    if obj not in enabled:
                        enabled.append(obj)

        return enabled

    def _scan_app_module(self, name):
        """

        Arguments:
            name (string):

        Returns:
            dict:
        """
        path = self.get_module_path(name)

        # Try to find application module and get its possible parameter variables
        module = self.find_app_module(path)
        if module:
            msg = "{klass} found application at: {path}".format(
                klass=self.__class__.__name__,
                path=path,
            )
            self.log.debug(msg)

            payload = {"name": name}

            if hasattr(module, "DEPENDENCIES"):
                payload["dependencies"] = getattr(module, "DEPENDENCIES")

            if hasattr(module, "PUSH_END"):
                payload["push_end"] = getattr(module, "PUSH_END")

            return payload

        return None

    def resolve_collection(self, lazy=True):
        """
        Resolve collection with AppStore.

        Keyword Arguments:
            lazy (boolean): If True, there won't be any dependency order resolving and
                the application list will just be the collection with AppNode objects.
                If False, the resolving will processed. Default is ``True``.

        Returns:
            list: List of AppNode.
        """
        collection = []

        for name in self.manifest.collection:
            payload = self._scan_app_module(name)
            # Ignore unfound application
            if payload:
                collection.append(payload)

        if lazy:
            self.apps = self.store.resolve(
                collection,
                no_ordering=True
            )
        else:
            self.apps = self.store.resolve(
                collection,
                no_ordering=self.manifest.no_ordering
            )
