
class AppNode:
    """
    Class to store application payload as an object.

    Arguments:
        name (string): The application module name.

    Keyword Arguments:
        push_end (boolean): Application parameter to describe that it should be pushed
            to end of the ordered application list.

    Attributes:
        name (string): The application name comes from its directory name in
            application repository.
        dependencies (list): List of AppNode objects. Only filled once ``AppStore``
            resolving has been done.
        dependency_names (list): List of string names. It is mostly used in
            ``AppStore`` preparation until it has done resolving.
        push_end (boolean): "Push end" mode value.
    """
    def __init__(self, name, push_end=False):
        self.name = name
        self.dependencies = []
        self.dependency_names = []
        self.push_end = push_end

    def __repr__(self):
        return "<{klass}: {name}>".format(
            klass=self.__class__.__name__,
            name=self.name
        )

    def __str__(self):
        return self.name

    def add_dependency(self, node):
        """
        Add a dependency object to the object registry ``AppNode.dependencies``.

        A dependency which already exists in registry is not added twice.

        Arguments:
            node (AppNode): Dependency object to add.
        """
        if node.name not in [item.name for item in self.dependencies]:
            self.dependencies.append(node)

    def add_dependency_name(self, name):
        """
        Add a dependency name to the name registry ``AppNode.dependency_names``.

        A dependency name which already exists in registry is not added twice.

        Arguments:
            node (string): Dependency name to add.
        """
        if name not in self.dependency_names:
            self.dependency_names.append(name)

    def to_dict(self, flat=False):
        """
        Serialize the object attribute as a dictionnary.

        Keyword Arguments:
            flat (boolean): If set to True, the dependencies are returned as a list of
                names (string) instead of AppNode objects.

        Returns:
            dict: Application payload including dependencies as ``AppNode`` objects.
        """
        return {
            "name": self.name,
            "dependencies": [
                dependency.name if flat is True else dependency
                for dependency in self.dependencies
            ],
            "push_end": self.push_end,
        }

    def to_payload(self):
        """
        Shortcut to ``to_dict`` with flat mode enforced.

        Returns:
            dict: Application payload including dependencies as string name.
        """
        return self.to_dict(flat=True)
