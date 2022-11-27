from pathlib import Path

from project_composer.compose import Composer


def check_project(manifest, processors=[], lazy=True):
    """
    Launch composer debugging check on a project.
    """
    manifest = Path(manifest).resolve()

    _composer = Composer(
        manifest,
        processors=processors,
    )

    _composer.check(lazy=lazy)
