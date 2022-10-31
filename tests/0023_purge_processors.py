import logging

import pytest

from project_composer.compose import Composer
from project_composer.processors import PurgeProcessor
from project_composer.exceptions import ComposerPurgeError


def test_purge_export_success(pytester, caplog, settings, basic_structure):
    """
    Purge export should return every Path object for module directories to remove
    from applications repository
    """
    caplog.set_level(logging.DEBUG)

    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer(
        {
            "name": "Sample",
            "collection": ["ping", "foo"],
            "repository": "basic_structure",
        },
        processors=[PurgeProcessor],
    )
    composer.resolve_collection(lazy=False)

    # Get the class names to avoid importing module classes for assertions
    dirnames = [
        item.name
        for item in composer.call_processor("PurgeProcessor", "export")
    ]

    assert sorted(dirnames) == ["bar", "dummy", "empty", "invalid", "pong"]

    assert [log[2] for log in caplog.record_tuples] == [
        "Composer found application at: basic_structure.ping",
        "Composer found application at: basic_structure.foo",
    ]


def test_purge_export_fail(pytester):
    """
    When the given repository module is not found from import_lib, it  will raises
    an exception 'ComposerPurgeError'
    """
    composer = Composer(
        {
            "name": "Sample",
            "collection": ["ping", "foo"],
            "repository": "not_importable_dummy_repository_module_path",
        },
        processors=[PurgeProcessor],
    )
    composer.resolve_collection(lazy=False)

    with pytest.raises(ComposerPurgeError):
        composer.call_processor("PurgeProcessor", "export")


def test_purge_commit(pytester, caplog, settings, basic_structure):
    """
    Purge commit should remove every module directories in repository that are not
    enabled applications from manifest.
    """
    caplog.set_level(logging.DEBUG)

    structure = basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer(
        {
            "name": "Sample",
            "collection": ["ping", "foo"],
            "repository": "basic_structure",
        },
        processors=[PurgeProcessor],
    )
    composer.resolve_collection(lazy=False)

    composer.call_processor("PurgeProcessor", "commit")

    remaining_module_dirs = sorted([
        item.name
        for item in structure.iterdir()
        if (item.is_dir() and not item.name.startswith("_"))
    ])

    assert remaining_module_dirs == ["foo", "ping"]

    assert [log[2] for log in caplog.record_tuples] == [
        "Composer found application at: basic_structure.ping",
        "Composer found application at: basic_structure.foo",
        "PurgeProcessor is removing application: {}/bar".format(structure),
        "PurgeProcessor is removing application: {}/pong".format(structure),
        "PurgeProcessor is removing application: {}/invalid".format(structure),
        "PurgeProcessor is removing application: {}/dummy".format(structure),
        "PurgeProcessor is removing application: {}/empty".format(structure),
    ]
