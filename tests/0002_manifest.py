import json

import pytest

from project_composer.exceptions import ComposerManifestError
from project_composer.manifest import RequirementsConfig, Manifest


def test_manifest_load_invalid_format(pytester, settings):
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


@pytest.mark.parametrize("manifest_filename, expected", [
    (
        "invalid_format.json",
        "Manifest 'apps' option is a required item and must be a list",
    ),
    (
        "invalid_format.toml",
        "Manifest 'apps' option is a required item and must be a list",
    ),
    (
        "invalid_pyproject.toml",
        "TOML manifest must have a section",
    ),
])
def test_manifest_load_invalid_json_format(settings, manifest_filename, expected):
    """
    Invalid syntax should raise a JSON error
    """
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    with pytest.raises(ComposerManifestError) as exc_info:
        Manifest.load(manifest_source)

    assert exc_info.value.args[0].startswith(expected) is True


@pytest.mark.parametrize(
    "manifest_filename, expected_name, expected_apps, expected_requirement",
    [
        (
            "basic.json",
            "Sample",
            [
                "foo",
                "bar",
                "ping",
                "nope",
            ],
            {
                "application_label": None,
                "application_divider": None,
                "dump": None,
                "introduction": RequirementsConfig._DEFAULT_INTRO,
                "source_filename": RequirementsConfig._DEFAULT_CONTENT_FILENAME,
                "template": None,
            },
        ),
        (
            "basic.toml",
            "Sample",
            [
                "foo",
                "bar",
                "ping",
                "nope",
            ],
            {
                "application_label": None,
                "application_divider": None,
                "dump": None,
                "introduction": RequirementsConfig._DEFAULT_INTRO,
                "source_filename": RequirementsConfig._DEFAULT_CONTENT_FILENAME,
                "template": None,
            },
        ),
        (
            "full.json",
            "Full manifest options",
            [
                "bar",
                "dummy",
                "empty",
                "foo",
                "ping",
                "pong",
                "nope",
            ],
            {
                "application_label": "# {name}\n",
                "application_divider": "\n",
                "dump": "output.txt",
                "introduction": None,
                "source_filename": RequirementsConfig._DEFAULT_CONTENT_FILENAME,
                "template": "requirements_template.txt",
            },
        ),
        (
            "full.toml",
            "Full manifest options",
            [
                "bar",
                "dummy",
                "empty",
                "foo",
                "ping",
                "pong",
                "nope",
            ],
            {
                "application_label": "# {name}\n",
                "application_divider": "\n",
                "dump": "output.txt",
                "introduction": None,
                "source_filename": RequirementsConfig._DEFAULT_CONTENT_FILENAME,
                "template": "requirements_template.txt",
            },
        ),
    ]
)
def test_manifest_load(settings, manifest_filename, expected_name, expected_apps,
                       expected_requirement):
    """
    Manifest should load a valid file and correctly fill its attribute from content,
    no matter what format backend is used.
    """
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename
    manifest = Manifest.load(manifest_source)

    assert manifest.name == expected_name
    assert manifest.apps == expected_apps

    # It's easier to test requirements config as dict against expected data
    requirements_kwargs = {
        k: getattr(manifest.requirements, k)
        for k in RequirementsConfig._FIELDS
    }

    assert requirements_kwargs == expected_requirement
