import logging

import pytest

from project_composer import __pkgname__
from project_composer.compose import PurgeApplications
from project_composer.exceptions import ComposerPurgeError


def test_purge_export_success(pytester, caplog, settings, basic_structure):
    """
    Purge export should return every Path object for module directories to remove
    from applications repository
    """
    caplog.set_level(logging.DEBUG)

    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    purger = PurgeApplications(
        {
            "name": "Sample",
            "collection": ["ping", "foo"],
            "repository": "basic_structure",
        },
    )

    # Get the class names to avoid importing module classes for assertions
    dirnames = [
        item.name
        for item in purger.export()
    ]

    assert sorted(dirnames) == ["bar", "dummy", "empty", "invalid", "pong"]

    assert caplog.record_tuples == [
        (
            __pkgname__,
            logging.DEBUG,
            "PurgeApplications found application at: basic_structure.ping"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "PurgeApplications found application at: basic_structure.foo"
        )
    ]


def test_purge_export_fail(pytester, caplog):
    """
    When the given repository module is not found from import_lib, it  will raises
    an exception 'ComposerPurgeError'
    """
    caplog.set_level(logging.DEBUG)

    purger = PurgeApplications(
        {
            "name": "Sample",
            "collection": ["ping", "foo"],
            "repository": "not_importable_dummy_repository_module_path",
        },
    )

    with pytest.raises(ComposerPurgeError):
        purger.export()


def test_purge_commit(pytester, caplog, settings, basic_structure):
    """
    Purge commit should remove every module directories in repository that are not
    enabled applications from manifest.
    """
    caplog.set_level(logging.DEBUG)

    structure = basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    purger = PurgeApplications(
        {
            "name": "Sample",
            "collection": ["ping", "foo"],
            "repository": "basic_structure",
        },
    )

    purger.commit()

    remaining_module_dirs = sorted([
        item.name
        for item in structure.iterdir()
        if (item.is_dir() and not item.name.startswith("_"))
    ])

    assert remaining_module_dirs == ["foo", "ping"]

    assert caplog.record_tuples == [
        (
            __pkgname__,
            logging.DEBUG,
            "PurgeApplications found application at: basic_structure.ping"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "PurgeApplications found application at: basic_structure.foo"
        ),
        (
            __pkgname__,
            logging.INFO,
            "PurgeApplications is removing application: {}/bar".format(structure)
        ),
        (
            __pkgname__,
            logging.INFO,
            "PurgeApplications is removing application: {}/pong".format(structure)
        ),
        (
            __pkgname__,
            logging.INFO,
            "PurgeApplications is removing application: {}/invalid".format(structure)
        ),
        (
            __pkgname__,
            logging.INFO,
            "PurgeApplications is removing application: {}/dummy".format(structure)
        ),
        (
            __pkgname__,
            logging.INFO,
            "PurgeApplications is removing application: {}/empty".format(structure)
        )
    ]
