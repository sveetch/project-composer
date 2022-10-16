import logging

import click

from .. import __pkgname__

from ..compose import PurgeApplications
from ..manifest import Manifest

from .base_options import COMMON_OPTIONS


@click.command()
@click.option(
    *COMMON_OPTIONS["manifest"]["args"],
    **COMMON_OPTIONS["manifest"]["kwargs"]
)
@click.option(
    *COMMON_OPTIONS["repository"]["args"],
    **COMMON_OPTIONS["repository"]["kwargs"]
)
@click.option(
    *COMMON_OPTIONS["syspaths"]["args"],
    **COMMON_OPTIONS["syspaths"]["kwargs"]
)
@click.option(
    "--commit",
    is_flag=True,
    help=(
        "Commit the purge."
    ),
)
@click.pass_context
def purge_command(*args, **parameters):
    """
    Purge applications repository from any directory that is not an enabled application
    module.

    Also the command cannot purge application directories that are not in application
    repository.

    WARNING: Once removed, the application directories cannot be retrieved.
    """
    logger = logging.getLogger(__pkgname__)

    logger.debug("Using manifest: {}".format(parameters["manifest"]))
    manifest = Manifest.load(parameters["manifest"])

    # Override base manifest settings from given arguments
    for name in manifest.get_fields():
        if name != "requirements" and parameters.get(name) is not None:
            setattr(manifest, name, parameters.get(name))

    if not manifest.repository:
        logger.critical(
            "Applications repository is required for this command, read help for "
            "more details."
        )
        raise click.Abort()

    # Logging used settings
    logger.debug("Applications repository: {}".format(manifest.repository))

    for item in manifest.syspaths:
        logger.debug("Loading in sys.path: {}".format(item))

    composer = PurgeApplications(manifest)

    commit = parameters.get("commit")
    if commit:
        to_remove = composer.commit()
    else:
        to_remove = composer.export()
        for path in to_remove:
            msg = "This application module would be removed: {}"
            logger.info(msg.format(path))

    if not to_remove:
        logger.warning("There was not any application module to remove")
