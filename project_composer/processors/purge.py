import shutil
from pathlib import Path

from ..importer import import_module

from .base import ComposerProcessor
from ..exceptions import ComposerPurgeError


class PurgeProcessor(ComposerProcessor):
    """
    Processor to purge application repository from not enabled application.

    This processor requires the repository to be set and valid.
    """
    def export(self):
        """
        Export module directory paths that should be purged from repository.

        Returns:
            list: A list of Path objects.
        """
        try:
            repository = import_module(self.composer.manifest.repository)
        except ModuleNotFoundError:
            msg = "{klass} is unable to find application repository module from: {path}"
            raise ComposerPurgeError(msg.format(
                klass=self.__class__.__name__,
                path=self.composer.manifest.repository,
            ))

        repository_path = Path(repository.__file__).parent

        # List module directories from repository and filter out the ones with a name
        # starting with "_"
        appdirs = [
            child
            for child in repository_path.iterdir()
            if (child.is_dir() and not child.name.startswith("_"))
        ]

        # Filter out the application module directories that are enabled from manifest
        return [
            item
            for item in appdirs
            if item.name not in [a.name for a in self.composer.apps]
        ]

    def commit(self):
        """
        Commit repository purge.
        """
        to_remove = self.export()

        for path in to_remove:
            msg = "{klass} is removing application: {path}".format(
                klass=self.__class__.__name__,
                path=path,
            )
            self.composer.log.info(msg)
            shutil.rmtree(path)

        return to_remove
