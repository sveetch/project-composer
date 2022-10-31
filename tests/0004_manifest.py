import json

import pytest

from project_composer.exceptions import ComposerManifestError, ComposerConfigError
from project_composer.manifest import RequirementsConfig, Manifest


def test_manifest_to_dict():
    """
    Manifest object should correctly dump all its field values to a dictionnary.
    """
    manifest = Manifest(
        name="foo",
        collection=["bar"],
        repository="plop.plip",
        syspaths=["flip", "flop", "flip"],
        default_store_app="base",
        no_ordering=False,
        requirements=RequirementsConfig(
            application_label="label",
            application_divider="div",
            template="template.txt",
            source_filename="source.txt",
            introduction="intro",
        ),
    )

    content = manifest.to_dict()

    assert content == {
        "name": "foo",
        "collection": ["bar"],
        "repository": "plop.plip",
        "default_store_app": "base",
        "no_ordering": False,
        "syspaths": [
            "flip",
            "flop",
            "flip"
        ],
        "requirements": {
            "application_label": "label",
            "application_divider": "div",
            "introduction": "intro",
            "source_filename": "source.txt",
            "template": "template.txt"
        }
    }


def test_manifest_load_unknow_format(pytester, settings):
    """
    Manifest filepath must have the right extension to guess its format
    """
    with pytest.raises(ComposerManifestError) as exc_info:
        Manifest.load("plop")

    msg = "Unable to guess the manifest file format"
    assert exc_info.value.args[0].startswith(msg) is True


def test_manifest_load_invalid_json_syntax(settings):
    """
    Invalid syntax should raise a JSON error
    """
    manifest_filename = "invalid_syntax.json"
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    with pytest.raises(json.decoder.JSONDecodeError):
        Manifest.load(manifest_source)


@pytest.mark.parametrize("manifest_filename, exception, expected", [
    (
        "invalid_format.json",
        ComposerConfigError,
        "Field 'collection' is required from 'Manifest'",
    ),
    (
        "invalid_format.toml",
        ComposerConfigError,
        "Field 'collection' is required from 'Manifest'",
    ),
    (
        "invalid_pyproject.toml",
        ComposerManifestError,
        (
            "TOML manifest must have a section [tool.project_composer] to fill base "
            "options."
        ),
    ),
])
def test_manifest_load_invalid_format(settings, manifest_filename, exception, expected):
    """
    Invalid syntax should raise a manifest error
    """
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    with pytest.raises(exception) as exc_info:
        Manifest.load(manifest_source)

    assert exc_info.value.args[0] == expected


@pytest.mark.parametrize("manifest_filename, expected", [
    (
        "basic.json",
        {
            "name": "Sample",
            "collection": [
                "foo",
                "bar",
                "ping",
                "nope",
            ],
            "repository": "basic_structure",
            "syspaths": [],
            "default_store_app": None,
            "no_ordering": False,
            "requirements": {
                "application_label": None,
                "application_divider": None,
                "introduction": RequirementsConfig._DEFAULT_INTRO,
                "source_filename": RequirementsConfig._DEFAULT_CONTENT_FILENAME,
                "template": None,
            }
        },
    ),
    (
        "basic.toml",
        {
            "name": "Sample",
            "collection": [
                "foo",
                "bar",
                "ping",
                "nope",
            ],
            "repository": "basic_structure",
            "syspaths": [],
            "default_store_app": None,
            "no_ordering": False,
            "requirements": {
                "application_label": None,
                "application_divider": None,
                "introduction": RequirementsConfig._DEFAULT_INTRO,
                "source_filename": RequirementsConfig._DEFAULT_CONTENT_FILENAME,
                "template": None,
            }
        },
    ),
    (
        "full.json",
        {
            "name": "Full manifest JSON",
            "collection": [
                "bar",
                "dummy",
                "empty",
                "foo",
                "ping",
                "pong",
                "nope",
            ],
            "repository": "basic_structure",
            "syspaths": ["container"],
            "default_store_app": "foo",
            "no_ordering": False,
            "requirements": {
                "application_label": "# {name}\n",
                "application_divider": "\n",
                "introduction": "",
                "source_filename": RequirementsConfig._DEFAULT_CONTENT_FILENAME,
                "template": "requirements_template.txt",
            }
        },
    ),
    (
        "full.toml",
        {
            "name": "Full manifest TOML",
            "collection": [
                "bar",
                "dummy",
                "empty",
                "foo",
                "ping",
                "pong",
                "nope",
            ],
            "repository": "basic_structure",
            "syspaths": ["container"],
            "default_store_app": "foo",
            "no_ordering": False,
            "requirements": {
                "application_label": "# {name}\n",
                "application_divider": "\n",
                "introduction": "",
                "source_filename": RequirementsConfig._DEFAULT_CONTENT_FILENAME,
                "template": "requirements_template.txt",
            }
        },
    ),
])
def test_manifest_load(settings, manifest_filename, expected):
    """
    Manifest should load a valid file and correctly fill its attribute from content,
    no matter what format backend is used.
    """
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename
    manifest = Manifest.load(manifest_source)

    assert manifest.to_dict() == expected
