"""
AppStore is in charge to store application collection, process it to translate
apps as AppNode objects and resolve application order following criterias.

Order criterias are:

* Natural list order which is a soft ordering because it is only respected after other
  criterias;
* Dependency, basically an application occurs after its dependencies;
* Parameter ``push_end`` to push an application after other applications that don't set
  it to True;

Parameter ``push_end`` is the strongest criterias but it does not break the dependency
ordering, so an app follow its dependencies if they are in `push_end`` mode.

Commonly, the `push_end` is to reserve to some very special applications and you
should prefer to lean on natural order and dependency order. If you use it, it is
recommended to use it the less possible because it may prooduces a cascade of
re-ordering you won't be able to fully control.

This is inspired by the algorith from "Ferry Boender":

https://www.electricmonk.nl/docs/dependency_resolving_algorithm/

"""
from ..exceptions import ComposerAppStoreError

from .node import AppNode


class AppStore:
    """
    Store a collection of applications and manage their dependencies.

    Application collection is a list of dictionnaries with the following structure: ::

        [
            {
                "name": String,
                "push_end": Boolean,
                "dependencies": List[String..]
            },
        ]

    Internally, every application are stored as an ``AppNode`` object.

    Keyword Arguments:
        default_app (string): Application name to attach as dependencies for
            applications that don't have any dependency. The name must exists in given
            collection. By default no default dependency is applied.

    Attributes:
        default_app (string): The value of ``default_app`` argument.
        processed_apps (list): Internal list of processed applications (translated to
            AppNode) filled by ``AppStore.process_collection()``.

    """
    def __init__(self, default_app=None):
        self.default_app = default_app
        self.processed_apps = []

    def get_app(self, name, default=None):
        """
        Get an app object from processed app list.

        Arguments:
            name (string): The name to get from processed applications.

        Keyword Arguments:
            default (object): Default value to use when given name is not retrieved
                from processed applications.

        Returns:
            AppNode: Application object.
        """
        return next(
            (app for app in self.processed_apps if app.name == name),
            default
        )

    def process_collection(self, collection):
        """
        Correctly store a collection of apps.

        This must be called before "resolve" since it register app nodes before linking
        their node dependencies.

        Also this is linear workflow only, at this point the list is not safe for
        circular references.

        Arguments:
            collection (list): List of application datas. Each app data must have a non
                empty ``name`` item. Also accept an optional item ``dependencies``
                which is a list of dependency names and an optional ``push_end`` item.
        """
        # First collect every app with their parameters as an Appnode in registry
        # At this stage app dependencies are only stored as name strings since not all
        # dependencies are yet registered as AppNode
        for item in collection:
            if self.get_app(item.get("name")):
                msg = (
                    "Application '{}' have multiple references in collection."
                )
                raise ComposerAppStoreError(msg.format(item.get("name")))

            node = AppNode(
                item.get("name"),
                push_end=item.get("push_end", False),
            )

            for name in item.get("dependencies", []):
                node.add_dependency_name(name)

            # Append the default dependency when app does not have any
            if (
                self.default_app and
                len(node.dependency_names) == 0 and
                self.default_app != node.name and
                self.default_app not in node.dependency_names
            ):
                node.add_dependency_name(self.default_app)

            self.processed_apps.append(node)

        # Then walk in processed apps to translate their dependency names with
        # registered AppNode
        for app in self.processed_apps:
            for name in app.dependency_names:
                node = self.get_app(name)

                if node:
                    app.add_dependency(node)
                else:
                    msg = (
                        "Dependency '{dep}' from application '{app}' is not a "
                        "registered application."
                    )
                    raise ComposerAppStoreError(msg.format(dep=name, app=app))

    def _apply_recursing_inheritance(self, app):
        """
        Apply dependencies 'push_end' inheritage.

        This will recursively walk into app's dependencies to search for any dependency
        app with 'push_end' to True and if true apply it on app.

        Arguments:
            app (AppNode): Application object to dig in for its dependency inheritance.
        """
        # Apply inheritance if any dep has push_end to True
        if len([
            item.name
            for item in app.dependencies
            if item.push_end
        ]) > 0:
            app.push_end = True

        # Follow dependencies to continue inheritance discovery
        for dep in app.dependencies:
            self._apply_recursing_inheritance(dep)

    def dependency_resolver(self, node, resolved, unresolved):
        """
        Recursive dependency resolver.

        This follow application dependencies to position them in the resolved list
        such a dependency is always after the application which require it.

        Arguments:
            node (AppNode): Application object to walk in.
            resolved (list): List of resolved application objects. Updated during
                resolving. This is commonly the value you will use to get the resolved
                and ordered applications.
            unresolved (list): List of unresolved application objects. Updated during
                resolving.
        """
        unresolved.append(node)

        for dependency in node.dependencies:
            if dependency not in resolved:
                if dependency in unresolved:
                    msg = "Circular reference detected: {source} -> {to}"
                    raise ComposerAppStoreError(
                        msg.format(source=node.name, to=dependency.name)
                    )
                self.dependency_resolver(dependency, resolved, unresolved)

        resolved.append(node)
        unresolved.remove(node)

    def resolve(self, collection, flat=False, no_ordering=False):
        """
        Resolve app list in order of app dependencies such as an app is always after
        all its dependencies.

        Arguments:
            collection (list): List of application payloads to work on.

        Keyword Arguments:
            flat (boolean): If True, returned list will be AppNode payload. Default to
                False.
            no_ordering (boolean): If ``True`` the ``AppStore.resolve()`` directly
                return the AppNode list with original order from collection. There
                won't be any resolution. Default is ``False``.

        Returns:
            list: List of AppNode object or payload (dict) respectively depending flat
            mode is False or True.
        """
        resolved = []

        # Process given application collection to translate them to AppNode with their
        # right parameters
        self.process_collection(collection)

        # By pass further resolving to return the app list ordered with its natural
        # order
        if no_ordering:
            ordered_resolve = self.processed_apps
        # Proceed to the last resolving actions
        else:
            # Go recursively resolve apps order with implied order by dependency
            for node in self.processed_apps:
                if node.name not in [r.name for r in resolved]:
                    self.dependency_resolver(node, resolved, [])

            # Apply possible dependencies parameters inheritance
            for app in resolved:
                self._apply_recursing_inheritance(app)

            # Consume resolved list to distinct apps with push_end=False from those
            # with push=True, built two distinct lists that are then joined (False
            # first, True last).
            ordered_resolve = [
                item
                for item in resolved
                if item.push_end is False
            ] + [
                item
                for item in resolved
                if item.push_end is True
            ]

        if flat:
            return [item.name for item in ordered_resolve]
        else:
            return ordered_resolve
