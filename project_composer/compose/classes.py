from .base import ComposerBase


class ClassComposer(ComposerBase):
    """
    Class composer find all existing classes for enabled application modules and that
    match criterias from ``_is_elligible_class``.
    """
    def export(self):
        """
        Export enabled applications classes.

        Returns:
            list: A list of Python classes found as elligible for criterias. The list
            is firstly ordered by the order of enabled application from manifest and
            secondly by their definition order in their module (if there is two classes
            defined with the same name, the first is retained and the second one is
            ignored).
        """
        mods = []
        _mod_names = set([])

        for node in self.apps:
            path = self.get_module_path(node.name)

            # Try to find module
            module = self.find_app_module(path)
            if module:
                msg = "{klass} found module at: {path}".format(
                    klass=self.__class__.__name__,
                    path=path,
                )
                self.log.debug(msg)

                mods.extend([
                    item
                    for item in self._get_elligible_module_classes(path, module)
                    if item.__name__ not in _mod_names
                ])
                # Update the list of unique retained class names which are used
                # for previous uniqueness comparaison in next iteration
                _mod_names.update([item.__name__ for item in mods])

        return mods
