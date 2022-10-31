import logging

from project_composer.compose import Composer
from project_composer.processors import ClassProcessor


def test_processor_class(caplog, pytester, basic_structure):
    """
    Processor should correctly find enabled class from application modules.
    """
    caplog.set_level(logging.DEBUG)

    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer(
        {
            "name": "Sample",
            "collection": ["ping", "pong", "foo", "dummy", "empty", "bar"],
            "repository": "basic_structure",
        },
        processors=[ClassProcessor],
    )
    composer.resolve_collection(lazy=False)

    # Get the class names to avoid importing module classes for assertions
    class_names = [
        item.__name__
        for item in composer.call_processor("ClassProcessor", "export")
    ]

    assert class_names == [
        "FooPlopInit",
        "FooPlapInit",
        "BarPlopInit",
        "BarPlapInit"
    ]

    # Don't bother about logger name and log level, only messages
    assert [log[2] for log in caplog.record_tuples] == [
        "Composer found application at: basic_structure.ping",
        "Composer found application at: basic_structure.pong",
        "Composer found application at: basic_structure.foo",
        "Composer found application at: basic_structure.dummy",
        "Composer found application at: basic_structure.empty",
        "Composer found application at: basic_structure.bar",
        "ClassProcessor found module at: basic_structure.ping",
        "ClassProcessor found module at: basic_structure.pong",
        "ClassProcessor found module at: basic_structure.foo",
        "Composer found enabled Class at: basic_structure.foo.FooPlopInit",
        "Composer found enabled Class at: basic_structure.foo.FooPlapInit",
        "ClassProcessor found module at: basic_structure.dummy",
        "ClassProcessor found module at: basic_structure.empty",
        "ClassProcessor found module at: basic_structure.bar",
        "Composer found enabled Class at: basic_structure.bar.BarPlopInit",
        "Composer found enabled Class at: basic_structure.bar.BarPlapInit"
    ]
