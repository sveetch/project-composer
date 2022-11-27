
class ComposerProcessor:
    """
    The base processor class to implement.

    This processor does not do anything nor have any real methods to call from
    composer.

    Arguments:
        composer (Composer): The composer instance where this processor will be
            executed.

    Attributes:
        composer (Composer): The composer instance used by processor to get manifest
            object and some internal composer methods to work with application
            repository.
    """
    def __init__(self, composer):
        self.composer = composer

    def get_module_path(self, name):
        """
        Return a Python path for a specific module name base on base application path
        from composer.

        This default implementation just use the base application module (``__init__``).
        Other processors may override it to use a specific module.

        Arguments:
            name (string): Module name.

        Returns:
            string: Module name prefixed with repository path if it is not empty else
            returns just the module name.
        """
        return self.composer.get_application_base_module_path(name)

    def check(self, printer=print):
        """
        Empty debugging check to implement on processors.
        """
        return []
