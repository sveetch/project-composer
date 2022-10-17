import logging

from project_composer import __pkgname__
from project_composer.compose import ClassComposer


def test_classcomposer_export_success(caplog, pytester, basic_structure):
    """
    Class composer should export all elligible classes from enable apps from manifest
    and conserve the class definition order.
    """
    caplog.set_level(logging.DEBUG)

    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = ClassComposer({
        "name": "Sample",
        "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
        "repository": "basic_structure",
    })

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
            "ClassComposer found application at: basic_structure.ping"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found application at: basic_structure.pong"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found application at: basic_structure.foo"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found application at: basic_structure.dummy"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found application at: basic_structure.empty"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found application at: basic_structure.bar"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found module at: basic_structure.ping"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found module at: basic_structure.pong"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found module at: basic_structure.foo"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found enabled Class at: basic_structure.foo.FooPlopInit"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found enabled Class at: basic_structure.foo.FooPlapInit"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found module at: basic_structure.dummy"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found module at: basic_structure.empty"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found module at: basic_structure.bar"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found enabled Class at: basic_structure.bar.BarPlopInit"
        ),
        (
            __pkgname__,
            logging.DEBUG,
            "ClassComposer found enabled Class at: basic_structure.bar.BarPlapInit"
        )
    ]
