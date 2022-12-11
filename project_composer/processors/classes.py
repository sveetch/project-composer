from .base import ComposerProcessor


class ClassProcessor(ComposerProcessor):
    """
    Class composer find all existing classes for enabled application modules and that
    match criterias from ``Composer._is_elligible_class``.
    """
    def export(self, **kwargs):
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

        for node in self.composer.apps:
            path = self.get_module_path(node.name)

            # Try to find module
            module = self.composer.find_app_module(path)
            if module:
                msg = "{klass} found module at: {path}".format(
                    klass=self.__class__.__name__,
                    path=path,
                )
                self.composer.log.debug(msg)

                mods.extend([
                    item
                    for item in self.composer._get_elligible_module_classes(path,
                                                                            module)
                    if item.__name__ not in _mod_names
                ])
                # Update the list of unique retained class names which are used
                # for previous uniqueness comparaison in next iteration
                _mod_names.update([item.__name__ for item in mods])

        return mods

    def check(self, printer=print):
        """
        Debugging check what this processor should find or match.

        Keyword Arguments:
            printer (callable): A callable to use to output debugging informations.
                Default to builtin function ``print`` but it won't be very pretty,
                we recommend to use ``utils.tree_printer.TreePrinter`` to benefit from
                the tree alike display. Note than composer already give ``TreePrinter``
                to this argument when calling this method.
        """
        printer()
        printer("🧵 Processor '{}'".format(self.__class__.__name__))

        app_last = len(self.composer.apps)
        for i, node in enumerate(self.composer.apps, start=1):
            printer(
                "X" if (i == app_last) else "T",
                node.name
            )
            path = self.get_module_path(node.name)
            module = self.composer.find_app_module(path)

            if module:
                klasses = self.composer._get_elligible_module_classes(path, module)
                klass_last = len(klasses)
                for k, item in enumerate(klasses, start=1):
                    printer(
                        (
                            "O" if (i == app_last) else "I"
                        ) + (
                            "X" if (k == klass_last) else "T"
                        ),
                        item.__name__
                    )
            else:
                pass
