import json

import pytest

from project_composer.compose import ComposerBase
from project_composer.exceptions import ProjectComposerException

from tests.data_fixtures.apps_structure import dummy as dummy_settings
from tests.data_fixtures.apps_structure.foo import settings as foo_settings
from tests.data_fixtures.apps_structure.bar import settings as bar_settings


def test_manifest_valid(settings):
    """
    Valid manifest file should load without errors
    """
    manifest_path = settings.fixtures_path / "manifests" / "basic.json"

    # Expected content from basic manifest, also used for the "direct manifest
    # dictionnary" way for manifest_path argument.
    manifest = {
        "name": "Sample",
        "apps": [
            "foo",
            "bar",
            "ping",
            "nope"
        ]
    }

    composer = ComposerBase(manifest_path, None)

    assert composer.manifest == manifest

    # Directly give a dictionnary instead of a path
    composer = ComposerBase(manifest, None)
    assert composer.manifest == manifest


def test_manifest_invalid_syntax(settings):
    """
    Invalid syntax should raise a JSON error
    """
    manifest_path = settings.fixtures_path / "manifests" / "invalid_syntax.json"

    with pytest.raises(json.decoder.JSONDecodeError):
        ComposerBase(manifest_path, None)


def test_manifest_invalid_format(settings):
    """
    Invalid format should raise a custom exception
    """
    manifest_path = settings.fixtures_path / "manifests" / "invalid_format.json"

    with pytest.raises(ProjectComposerException):
        ComposerBase(manifest_path, None)

    with pytest.raises(ProjectComposerException):
        ComposerBase({"nope": True}, None)


@pytest.mark.parametrize("appsdir_pythonpath, name, expected", [
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
def test_get_module_path(appsdir_pythonpath, name, expected):
    """
    Method should return the right expected path depending composer attribute
    'appsdir_pythonpath' value.
    """
    composer = ComposerBase(
        {"name": "Sample", "apps": []},
        appsdir_pythonpath
    )
    assert composer.get_module_path(name) == expected


def test_find_app_module_notfound():
    """
    Importation should fail without exception but still emit a warning log
    """
    composer = ComposerBase({"name": "Sample", "apps": []}, None)

    module_path = composer.get_module_path("foo")
    assert composer.find_app_module(module_path) is None


def test_find_app_module_success():
    """
    Importation should succeed when the module is available.
    """
    composer = ComposerBase(
        {"name": "Sample", "apps": []},
        "tests.data_fixtures.apps_structure"
    )

    module_path = composer.get_module_path("foo")
    assert composer.find_app_module(module_path) is not None
    assert composer.find_app_module(module_path).__name__ == module_path


def test_find_app_module_invalid():
    """
    Invalid module still raises exception because it must be explicit.
    """
    composer = ComposerBase(
        {"name": "Sample", "apps": []},
        "tests.data_fixtures.apps_structure"
    )

    module_path = composer.get_module_path("invalid")

    with pytest.raises(NameError):
        assert composer.find_app_module(module_path)


def test_get_elligible_module_classes():
    """
    All EnabledApplicationMarker inheriters from a module should be found as elligible.
    """
    composer = ComposerBase({"name": "Sample", "apps": []}, None)

    # There is no elligible class at the root of module "foo"
    classes = composer._get_elligible_module_classes("some.path", dummy_settings)
    assert classes == []

    # Foo settings have an elligible class
    classes = composer._get_elligible_module_classes("some.path", foo_settings)
    assert classes == [foo_settings.FooSettings]

    # Bar settings have multiple elligible classes
    classes = composer._get_elligible_module_classes("some.path", bar_settings)
    assert classes == [bar_settings.BarFirstSettings, bar_settings.BarSecondSettings]
