from ...processors import ClassProcessor


class DjangoSettingsProcessor(ClassProcessor):
    """
    Processor for enabled application settings classes for a Django project.
    """
    def get_module_path(self, name):
        """
        Return a Python path for a module name.

        Arguments:
            name (string): Module name.

        Returns:
            string: Module name prefixed with repository path if it is not empty else
            returns just the module name.
        """
        return "{base}.{part}".format(
            base=self.composer.get_application_base_module_path(name),
            part="settings",
        )


class DjangoUrlsProcessor(ClassProcessor):
    """
    Processor for enabled application urls classes for a Django project.
    """
    def get_module_path(self, name):
        """
        Return a Python path for a module name.

        Arguments:
            name (string): Module name.

        Returns:
            string: Module name prefixed with repository path if it is not empty else
            returns just the module name.
        """
        return "{base}.{part}".format(
            base=self.composer.get_application_base_module_path(name),
            part="urls",
        )
