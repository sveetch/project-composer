import logging

import click

from .. import __pkgname__

from ..compose import Composer
from ..manifest import Manifest
from ..processors import PurgeProcessor

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

    # Load manifest settings
    logger.debug("Using manifest: {}".format(parameters["manifest"]))
    manifest = Manifest.load(parameters["manifest"])

    # Patch arguments in multiple mode since an empty default list trouble the
    # manifest settings overriding
    if len(parameters.get("syspaths", [])) == 0:
        parameters["syspaths"] = None

    # Override base manifest settings from given arguments
    # syspaths management have a special thing to avoid default value (empty list) to
    # override the manifest value
    for name in manifest.get_fieldnames():
        if (name != "requirements" and parameters.get(name) is not None):
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

    composer = Composer(manifest, processors=[PurgeProcessor])
    composer.resolve_collection(lazy=False)

    commit = parameters.get("commit")
    if commit:
        to_remove = composer.call_processor("PurgeProcessor", "commit")
    else:
        to_remove = composer.call_processor("PurgeProcessor", "export")
        for path in to_remove:
            msg = "This application module would be removed: {}"
            logger.info(msg.format(path))

    if not to_remove:
        logger.warning("There was not any application module to remove")
