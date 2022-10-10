import logging

import click

from .. import __pkgname__

from ..compose import PurgeApplications

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
    *COMMON_OPTIONS["syspath"]["args"],
    **COMMON_OPTIONS["syspath"]["kwargs"]
)
@click.option(
    "--commit",
    is_flag=True,
    help=(
        "Commit the purge."
    ),
)
@click.pass_context
def purge_command(context, manifest, repository, syspath, commit):
    """
    Purge applications repository from any directory that is not an enabled application
    module.

    Also the command cannot purge application directories that are not in application
    repository.

    WARNING: Once removed, the application directories cannot be retrieved.
    """
    logger = logging.getLogger(__pkgname__)

    logger.debug("Using manifest: {}".format(manifest))

    if repository:
        logger.debug("Applications repository: {}".format(repository))
    else:
        logger.critical("Applications repository is required.")
        raise click.Abort()

    for item in syspath:
        logger.debug("Loading in sys.path: {}".format(item))

    composer = PurgeApplications(
        manifest,
        repository,
        base_syspaths=syspath,
    )

    if commit:
        to_remove = composer.commit()
    else:
        to_remove = composer.export()
        for path in to_remove:
            msg = "This application module would be removed: {}"
            logger.info(msg.format(path))

    if not to_remove:
        logger.warning("There was not any application module to remove")
