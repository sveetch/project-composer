import logging
from pathlib import Path

import click

from .. import __pkgname__

from ..compose import RequirementsComposer

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
    "--template",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    default=None,
    metavar="FILEPATH",
    help=(
        "File path to a base requirements file which will be extended (not "
        "overwritten) with application requirements. Ignore this argument if you "
        "want to start from scratch."
    ),
)
@click.option(
    "--dump",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, path_type=Path),
    default=None,
    metavar="FILEPATH",
    help=(
        "File path where to dump exported requirements combination from applications."
    ),
)
@click.option(
    "--minimal",
    is_flag=True,
    help=(
        "Forces all documents to be be parsed in buffered mode instead "
        "of streaming mode (causes some parse errors to be treated as "
        "non-fatal document errors instead of as fatal document errors)."
    ),
)
@click.pass_context
def requirements_command(context, manifest, repository, syspath, template, dump,
                         minimal):
    """
    Output composed requirements from applications.
    """
    logger = logging.getLogger(__pkgname__)

    composer_kwargs = {}

    logger.debug("Using manifest: {}".format(manifest))

    if repository:
        logger.debug("Applications repository: {}".format(repository))

    for item in syspath:
        logger.debug("Loading in sys.path: {}".format(item))

    if template:
        logger.debug("Using template: {}".format(template))

    if dump:
        logger.debug("Dump destination: {}".format(dump))

    if minimal:
        logger.debug("Minimalist output enabled")
        composer_kwargs.update({
            "application_label": None,
            "application_divider": None,
            "introduction": None,
        })

    composer = RequirementsComposer(
        manifest,
        repository,
        base_output=template,
        base_syspaths=syspath,
        **composer_kwargs
    )

    if dump:
        msg = "Requirements file written at: {}"
        logger.debug(msg.format(
            composer.dump(dump)
        ))
    else:
        click.echo(composer.export())
