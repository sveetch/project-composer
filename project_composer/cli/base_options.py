from pathlib import Path

import click

from ..defaults import DEFAULT_MANIFEST_PATH


# Shared options
COMMON_OPTIONS = {
    "manifest": {
        "args": ("--manifest",),
        "kwargs": {
            "type": click.Path(
                exists=True,
                file_okay=True,
                dir_okay=False,
                path_type=Path
            ),
            "default": DEFAULT_MANIFEST_PATH,
            "metavar": "FILEPATH",
            "help": (
                "Required file path to a project manifest."
            ),
        }
    },
    "repository": {
        "args": ("--repository",),
        "kwargs": {
            "default": None,
            "metavar": "PYTHONPATH",
            "help": (
                "A Python path (aka: 'foo.apps') where to search for application "
                "modules. Using this argument will override the 'repository' item from"
                "manifest."
            ),
        }
    },
    "syspaths": {
        "args": ("--syspath", "syspaths"),
        "kwargs": {
            "default": [],
            "multiple": True,
            "metavar": "DIRPATH",
            "help": (
                "Path to a directory to add to 'sys.path' and which contains Python "
                "modules required by some applications if not already available in the "
                "scope of this tool. You can define it multiple times for each needed "
                "path. Using this argument will override the 'syspaths' value from "
                "manifest."
            ),
        }
    },
}
