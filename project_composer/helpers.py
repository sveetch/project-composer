from pathlib import Path

from project_composer.compose import Composer


def check_project(manifest, processors=[], lazy=True):
    """
    Launch composer debugging on a project.

    Composer and processor check method do not return anything and just print out
    every debugging output.

    Arguments:
        manifest (pathlib.Path): Manifest Path object.

    Keyword Arguments:
        processors (list): List of processor to enable in composer.
        lazy (boolean): The composer ``lazy`` argument value to use.

    """
    manifest = Path(manifest).resolve()

    _composer = Composer(
        manifest,
        processors=processors,
    )

    _composer.check(lazy=lazy)
