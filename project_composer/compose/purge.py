"""
==============
Class composer
==============

"""
import shutil
from pathlib import Path

from ..importer import import_module

from .base import ComposerBase
from ..exceptions import ComposerPurgeError


class PurgeApplications(ComposerBase):
    """
    Class to use to purge application repository from not enabled application.

    Opposed to ComposerBase, this class indeed require the repository to be set and
    valid.
    """
    def export(self):
        """
        Export module directory paths.

        Returns:
            list: A list of Path objects.
        """
        try:
            repository = import_module(self.manifest.repository)
        except ModuleNotFoundError:
            msg = "Unable to find application repository module: {}"
            raise ComposerPurgeError(msg.format(self.manifest.repository))

        repository_path = Path(repository.__file__).parent

        # List module directories from repository and filter out the ones have a name
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
            if item.name not in self.manifest.apps
        ]

    def commit(self):
        """
        Commit repository purge.
        """
        to_remove = self.export()

        for path in to_remove:
            self.log.info("Removing application module: {}".format(path))
            shutil.rmtree(path)

        return to_remove