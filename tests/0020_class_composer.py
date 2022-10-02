import logging

from project_composer import __pkgname__
from project_composer.compose import ClassComposer


def test_classcomposer_export_success(caplog):
    """
    Class composer should export all elligible classes from enable apps from manifest
    and conserve the class definition order.
    """
    caplog.set_level(logging.DEBUG)

    composer = ClassComposer(
        {
            "name": "Sample",
            "apps": ["ping", "pong", "foo", "dummy", "empty", "bar"]
        },
        "tests.data_fixtures.apps_structure"
    )

    # Get the class names to avoid importing module classes for assertions
    class_names = [
        item.__name__
        for item in composer.export()
    ]

    assert class_names == ["FooPlopInit", "FooPlapInit", "BarPlopInit", "BarPlapInit"]

    assert caplog.record_tuples == [
        (
            __pkgname__,
            logging.DEBUG,
            "Found application module at: tests.data_fixtures.apps_structure.ping"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "Found application module at: tests.data_fixtures.apps_structure.pong"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "Found application module at: tests.data_fixtures.apps_structure.foo"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "Got enabled class at: tests.data_fixtures.apps_structure.foo.FooPlopInit"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "Got enabled class at: tests.data_fixtures.apps_structure.foo.FooPlapInit"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "Found application module at: tests.data_fixtures.apps_structure.dummy"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "Found application module at: tests.data_fixtures.apps_structure.empty"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "Found application module at: tests.data_fixtures.apps_structure.bar"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "Got enabled class at: tests.data_fixtures.apps_structure.bar.BarPlopInit"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "Got enabled class at: tests.data_fixtures.apps_structure.bar.BarPlapInit"
        )
    ]
