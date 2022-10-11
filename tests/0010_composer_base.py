import pytest

from project_composer.compose import ComposerBase
from project_composer.importer import import_module
from project_composer.manifest import Manifest


def test_manifest_valid_file(settings):
    """
    Valid manifest file should load without errors
    """
    manifest_path = settings.fixtures_path / "manifests" / "basic.json"

    composer = ComposerBase(manifest_path)

    assert composer.manifest.name == "Sample"
    assert composer.manifest.apps == [
        "foo",
        "bar",
        "ping",
        "nope"
    ]


def test_manifest_valid_model(settings):
    # Directly give a dictionnary instead of a path
    manifest = Manifest("Sample", [
        "foo",
        "bar",
        "ping",
        "nope"
    ])
    composer = ComposerBase(manifest)
    assert composer.manifest.name == "Sample"
    assert composer.manifest.apps == [
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
    composer = ComposerBase({
        "name": "Sample",
        "apps": [],
        "repository": repository,
    })
    assert composer.get_module_path(name) == expected


def test_find_app_module_notfound():
    """
    Importation should fail without exception but still emit a warning log
    """
    composer = ComposerBase({
        "name": "Sample",
        "apps": [],
    })

    module_path = composer.get_module_path("foo")
    assert composer.find_app_module(module_path) is None


def test_find_app_module_success():
    """
    Importation should succeed when the module is available.
    """
    composer = ComposerBase({
        "name": "Sample",
        "apps": [],
        "repository": "tests.data_fixtures.apps_structure",
    })

    module_path = composer.get_module_path("foo")
    found = composer.find_app_module(module_path)
    assert found is not None
    assert found.__name__ == module_path


def test_find_app_module_success2():
    """
    Importation should succeed when the module is available.
    """
    composer = ComposerBase({
        "name": "Sample",
        "apps": [],
        "repository": "tests.data_fixtures.apps_structure",
    })

    module_path = composer.get_module_path("foo")
    found = composer.find_app_module(module_path)
    assert found is not None
    assert found.__name__ == module_path


def test_find_app_module_invalid():
    """
    Invalid module still raises exception because it must be explicit.
    """
    composer = ComposerBase({
        "name": "Sample",
        "apps": [],
        "repository": "tests.data_fixtures.apps_structure",
    })

    module_path = composer.get_module_path("invalid")

    with pytest.raises(NameError):
        assert composer.find_app_module(module_path)


def test_get_elligible_module_classes(pytester, settings, install_structure):
    """
    All EnabledApplicationMarker inheriters from a module should be found as elligible.
    """
    install_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    composer = ComposerBase({"name": "Sample", "apps": []})

    dummy = import_module("apps_structure.dummy")
    foo_settings = import_module("apps_structure.foo.settings")
    bar_settings = import_module("apps_structure.bar.settings")

    # There is no elligible class at the root of module "foo"
    classes = composer._get_elligible_module_classes("some.path", dummy)
    assert classes == []

    # Foo settings have an elligible class
    classes = composer._get_elligible_module_classes("some.path", foo_settings)
    assert classes == [foo_settings.FooSettings]

    # Bar settings have multiple elligible classes
    classes = composer._get_elligible_module_classes("some.path", bar_settings)
    assert classes == [bar_settings.BarFirstSettings, bar_settings.BarSecondSettings]
