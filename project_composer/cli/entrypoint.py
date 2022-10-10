"""
Main entrance to commandline actions

Since Click use function docstring to build its help content, no command
function are documented.
"""
import click

from ..defaults import APP_LOGGER_CONF
from ..logger import init_logger

from .version import version_command
from .requirements import requirements_command
from .purge import purge_command


# Help alias on "-h" argument
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-v", "--verbose",
    type=click.IntRange(min=0, max=5),
    default=4,
    metavar="INTEGER",
    help=(
        "An integer between 0 and 5, where '0' make a totaly "
        "silent output and '5' set level to DEBUG (the most verbose "
        "level). Default to '4' (Info level)."
    )
)
@click.pass_context
def cli_frontend(ctx, verbose):
    """
    Project composer commandline interface
    """
    printout = True
    if verbose == 0:
        verbose = 1
        printout = False

    # Verbosity is the inverse of logging levels
    levels = [item for item in APP_LOGGER_CONF]
    levels.reverse()
    # Init the logger config
    root_logger = init_logger(
        "project-composer",
        levels[verbose],
        printout=printout
    )

    # Init the default context that will be passed to commands
    ctx.obj = {
        "verbosity": verbose,
        "logger": root_logger,
    }


# Attach commands methods to the main grouper
cli_frontend.add_command(version_command, name="version")
cli_frontend.add_command(requirements_command, name="requirements")
cli_frontend.add_command(purge_command, name="purge")
