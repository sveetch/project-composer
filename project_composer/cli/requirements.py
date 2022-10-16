import logging
from pathlib import Path

import click

from .. import __pkgname__

from ..compose import TextContentComposer
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
    "--applabel",
    "application_label",
    default=None,
    metavar="STRING",
    help=(
        "A string to add the application name before its requirements. The name will "
        "be added in expected pattern '{name}' Remember to finish you string with a"
        "newline character.."
    ),
)
@click.option(
    "--appdivider",
    "application_divider",
    default=None,
    metavar="STRING",
    help=(
        "String to add between application. Commonly used to insert a new line. "
        "By default there is no divider."
    ),
)
@click.option(
    "--introduction",
    default=None,
    metavar="STRING",
    help=(
        "Introduction string to start output. Accept a pattern '{creation_date}' to "
        "include the current date. Give an empty string to disable introduction. If "
        "argument is not defined a default introduction is included with a WARNING "
        "and the date."
    ),
)
@click.option(
    "--source",
    "source_filename",
    default=None,
    metavar="STRING",
    help=(
        "Filename to search in application module to find requirements."
    ),
)
@click.pass_context
def requirements_command(*args, **parameters):
    """
    Output composed requirements from applications.
    """
    logger = logging.getLogger(__pkgname__)

    # Load manifest settings
    logger.debug("Using manifest: {}".format(parameters["manifest"]))
    manifest = Manifest.load(parameters["manifest"])

    # Override base manifest settings from given arguments
    for name in manifest.get_fields():
        if name != "requirements" and parameters.get(name) is not None:
            setattr(manifest, name, parameters.get(name))
    # The same for requirements plugin
    for name in manifest.requirements.get_fields():
        if parameters.get(name) is not None:
            setattr(manifest.requirements, name, parameters.get(name))

    # Logging used settings
    if manifest.repository:
        logger.debug("Applications repository: {}".format(manifest.repository))

    for item in manifest.syspaths:
        logger.debug("Loading in sys.path: {}".format(item))

    logger.debug("Using template: {}".format(manifest.requirements.template))
    logger.debug("Using source filename: {}".format(
        manifest.requirements.source_filename)
    )

    composer = TextContentComposer(manifest)

    dump = parameters.get("dump")
    if dump:
        logger.debug("Dump destination: {}".format(dump))
        msg = "Requirements file written at: {}"
        logger.debug(msg.format(
            composer.dump(dump)
        ))
    else:
        click.echo(composer.export())
