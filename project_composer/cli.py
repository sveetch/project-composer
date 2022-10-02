import argparse
from pathlib import Path

from .logger import init_logger
from .compose import RequirementsComposer
from . import __pkgname__, __version__


# Default manifest is searched in current working directory
DEFAULT_MANIFEST_PATH = Path("./composition-manifest.json")

# Available logging levels
APP_LOGGER_CONF = (
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    None
)


def add_logger_arguments(parser):
    parser.add_argument(
        "-v", "--verbose",
        type=int,
        choices=range(0, len(APP_LOGGER_CONF)),
        default=5,
        metavar="INTEGER",
        help=(
            "An integer between 0 and 5, where '0' make a totaly "
            "silent output and '5' set level to DEBUG (the most verbose "
            "level). (default: %(default)s)"
        )
    )


def add_base_arguments(parser, default_manifest_path=None):
    parser.add_argument(
        "--mode",
        choices=["version", "requirements"],
        default="version",
        help=(
            "(version) Display version and exit. "
            "(requirements) Output or dump (depending options) composed requirements "
            "from applications."
        )
    )
    parser.add_argument(
        "--manifest",
        metavar="FILEPATH",
        default=default_manifest_path,
        help=(
            "Required file path to a project manifest. (default: %(default)s)"
        )
    )
    parser.add_argument(
        "--syspath",
        nargs="*",
        metavar="DIRPATH",
        help=(
            "Path to a directory to add to 'sys.path' and which contains Python "
            "modules required by some applications if not already available in the "
            "scope of this tool. You can define it multiple times for each needed "
            "path. (default: %(default)s)"
        )
    )
    parser.add_argument(
        "--appsdir",
        metavar="DIRPATH",
        help=(
            "Python path (aka: 'foo.apps') where to search for applications "
            "modules. (default: %(default)s)"
        )
    )


def add_requirements_arguments(parser):
    parser.add_argument(
        "--base",
        metavar="FILEPATH",
        help=(
            "(Requirements only) File path to a base requirements file which will be "
            "extended (not overwritten) with application requirements. Ignore this "
            "argument if you want to start from scratch. (default: %(default)s)"
        )
    )
    parser.add_argument(
        "--minimal",
        action="store_true",
        help=(
            "(Requirements only) Enable the minimal output format to disable "
            "introduction, application label and application divider when combining "
            "applications requirements. (default: %(default)s)"
        )
    )
    parser.add_argument(
        "--dump",
        metavar="FILEPATH",
        help=(
            "(Requirements only) File path where to dump exported requirements "
            "combination from applications. (default: %(default)s)"
        )
    )


def get_logger(parser, args):
    """
    Logging setup from verbosity arguments.
    """
    printout = True
    verbosity = args.verbose
    if verbosity == 0:
        verbosity = 1
        printout = False

    # Verbosity is the inverse of logging levels
    levels = [item for item in APP_LOGGER_CONF]
    levels.reverse()

    # Init the logger config
    return init_logger(
        __pkgname__,
        levels[verbosity],
        printout=printout,
    )


def get_manifest_path(logger, parser, args):
    """
    Validate and get manifest path
    """
    if not args.manifest:
        parser.error("Manifest file path is required.")

    manifest_path = Path(args.manifest)

    if not manifest_path.exists():
        parser.error("Unable to find manifest at: {}".format(manifest_path))

    logger.debug("Using manifest: {}".format(manifest_path))

    return manifest_path


def get_base_output_path(logger, parser, args):
    """
    Validate and get base output path
    """
    if not args.base:
        return None

    base_output_path = Path(args.base)

    logger.debug("Using base output from: {}".format(base_output_path))

    return base_output_path


def get_requirements_format_options(logger, parser, args):
    """
    Build keyword arguments for options related to requirements output formatting.
    """
    if not args.minimal:
        return {}

    return {
        "application_label": None,
        "application_divider": None,
        "introduction": None,
    }


def main():
    """
    Main commandline interface glues arguments definitions, validation and launching
    composer features.
    """
    parser = argparse.ArgumentParser(
        description="Project composer commandline",
    )
    add_logger_arguments(parser)
    add_base_arguments(parser, default_manifest_path=DEFAULT_MANIFEST_PATH)
    add_requirements_arguments(parser)
    args = parser.parse_args()

    # Version display
    if args.mode == "version":
        print("{} {}".format(__pkgname__, __version__))
        parser.exit()

    logger = get_logger(parser, args)
    manifest_path = get_manifest_path(logger, parser, args)

    # Possible options specific to composer implementations
    composer_kwargs = {}

    base_output_path = get_base_output_path(logger, parser, args)
    composer_kwargs.update(
        get_requirements_format_options(logger, parser, args)
    )

    if args.mode == "requirements":
        composer = RequirementsComposer(
            manifest_path,
            args.appsdir,
            base_output=base_output_path,
            **composer_kwargs
        )

        if args.dump:
            print(composer.destination(Path(args.dump)))
        else:
            print(composer.export())
