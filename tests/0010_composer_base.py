import pytest

from project_composer.compose import Composer
from project_composer.exceptions import ComposerError
from project_composer.importer import import_module
from project_composer.manifest import Manifest
from project_composer.processors import ComposerProcessor


def test_manifest_valid_file(settings):
    """
    Valid manifest file should load without errors
    """
    manifest_path = settings.fixtures_path / "manifests" / "basic.json"

    composer = Composer(manifest_path)

    assert composer.manifest.name == "Sample"
    assert composer.manifest.collection == [
        "foo",
        "bar",
        "ping",
        "nope"
    ]


def test_manifest_valid_model():
    # Directly give a dictionnary instead of a path
    manifest = Manifest(
        name="Sample",
        collection=[
            "foo",
            "bar",
            "ping",
            "nope"
        ],
        repository="foo",
    )
    composer = Composer(manifest)
    assert composer.manifest.name == "Sample"
    assert composer.manifest.collection == [
        "foo",
        "bar",
        "ping",
        "nope"
    ]


@pytest.mark.parametrize("repository, name, expected", [
    (
        None,
        "bar",
        "bar",
    ),
    (
        "foo",
        "bar",
        "foo.bar",
    ),
])
def test_get_module_path(repository, name, expected):
    """
    Method should return the right expected path depending composer attribute
    'repository' value.
    """
    composer = Composer({
        "name": "Sample",
        "collection": [],
        "repository": repository,
    })
    assert composer.get_module_path(name) == expected


def test_find_app_module_notfound():
    """
    Importation should fail without exception but still emit a warning log
    """
    composer = Composer({
        "name": "Sample",
        "collection": [],
        "repository": None,
    })

    module_path = composer.get_module_path("foo")
    assert composer.find_app_module(module_path) is None


def test_find_app_module_success(pytester, basic_structure):
    """
    Importation should succeed when the module is available.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer({
        "name": "Sample",
        "collection": [],
        "repository": "basic_structure",
    })

    module_path = composer.get_module_path("foo")
    found = composer.find_app_module(module_path)
    assert found is not None
    assert found.__name__ == module_path


def test_find_app_module_success2(pytester, basic_structure):
    """
    Importation should succeed when the module is available.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer({
        "name": "Sample",
        "collection": [],
        "repository": "basic_structure",
    })

    module_path = composer.get_module_path("foo")
    found = composer.find_app_module(module_path)
    assert found is not None
    assert found.__name__ == module_path


def test_find_app_module_invalid(pytester, basic_structure):
    """
    Invalid module still raises exception because it must be explicit.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer({
        "name": "Sample",
        "collection": [],
        "repository": "basic_structure",
    })

    module_path = composer.get_module_path("invalid")

    with pytest.raises(NameError):
        assert composer.find_app_module(module_path)


def test_call_processor_errors(pytester, basic_structure):
    """
    Method 'call_processor' should behaves as expected depending how it is used, with
    some internal validation.
    """
    class DummyProcessor(ComposerProcessor):
        def foo(self):
            return "Foo"

        def hello(self, **kwargs):
            return "Hello {}".format(kwargs.get("word"))

    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer(
        {
            "name": "Sample",
            "collection": [],
            "repository": "basic_structure",
        },
        processors=[DummyProcessor],
    )

    assert composer.call_processor("DummyProcessor", "foo") == "Foo"

    assert composer.call_processor("DummyProcessor", "hello", word="World") == (
        "Hello World"
    )

    with pytest.raises(ComposerError) as exc_info:
        composer.call_processor("NopeProcessor", "foo")

    assert exc_info.value.args[0] == (
        "Given processor name is not registered from composer: NopeProcessor"
    )

    with pytest.raises(ComposerError) as exc_info:
        composer.call_processor("DummyProcessor", "nope")

    assert exc_info.value.args[0] == (
        "Processor 'DummyProcessor' don't have any method named 'nope'"
    )


def test_get_elligible_module_classes(pytester, basic_structure):
    """
    All EnabledApplicationMarker inheriters from a module should be found as elligible.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = Composer({"name": "Sample", "collection": [], "repository": None})

    dummy = import_module("basic_structure.dummy")
    foo_settings = import_module("basic_structure.foo.settings")
    bar_settings = import_module("basic_structure.bar.settings")

    # There is no elligible class at the root of module "foo"
    classes = composer._get_elligible_module_classes("some.path", dummy)
    assert classes == []

    # Foo settings have an elligible class
    classes = composer._get_elligible_module_classes("some.path", foo_settings)
    assert classes == [foo_settings.FooSettings]

    # Bar settings have multiple elligible classes
    classes = composer._get_elligible_module_classes("some.path", bar_settings)
    assert classes == [bar_settings.BarFirstSettings, bar_settings.BarSecondSettings]


@pytest.mark.parametrize("default_app, no_ordering, lazy, expected", [
    (
        None,
        False,
        False,
        [
            "forms",
            "editor",
            "filer",
            "django",
            "blog",
            "rest",
            "cms",
            "cms_blog",
        ],
    ),
    (
        "django",
        False,
        False,
        [
            "django",
            "forms",
            "editor",
            "filer",
            "blog",
            "rest",
            "cms",
            "cms_blog",
        ],
    ),
    (
        None,
        True,
        False,
        [
            "cms",
            "django",
            "forms",
            "filer",
            "editor",
            "blog",
            "rest",
            "cms_blog"
        ],
    ),
    (
        None,
        False,
        True,
        [
            "cms",
            "django",
            "forms",
            "filer",
            "editor",
            "blog",
            "rest",
            "cms_blog"
        ],
    ),
    (
        None,
        True,
        True,
        [
            "cms",
            "django",
            "forms",
            "filer",
            "editor",
            "blog",
            "rest",
            "cms_blog"
        ],
    ),
    (
        "django",
        True,
        True,
        [
            "cms",
            "django",
            "forms",
            "filer",
            "editor",
            "blog",
            "rest",
            "cms_blog"
        ],
    ),
])
def test_composer_resolve_apps(pytester, advanced_structure, default_app, no_ordering,
                               lazy, expected):
    """
    Composer should set the right app list depending parameters.
    """
    advanced_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    # Craft manifest
    manifest = Manifest(
        name="Advanced",
        collection=[
            "nope",
            "cms",
            "django",
            "forms",
            "filer",
            "editor",
            "blog",
            "rest",
            "cms_blog",
        ],
        default_store_app=default_app,
        no_ordering=no_ordering,
        repository="advanced_structure",
    )

    # Start composer which will immediately proceed to resolve
    composer = Composer(manifest)
    composer.resolve_collection(lazy=lazy)

    assert [item.name for item in composer.apps] == expected
