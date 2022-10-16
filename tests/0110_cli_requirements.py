import logging
from pathlib import Path

import pytest

from click.testing import CliRunner

from freezegun import freeze_time

from project_composer import __pkgname__
from project_composer.cli.entrypoint import cli_frontend
from project_composer.utils.tests import debug_invoke
from project_composer.manifest import Manifest


def test_requirements_manifest_opt_fail(caplog):
    """
    Command require at least the manifest option and its default value should fail when
    there is not expect manifest file in current working directory
    """
    runner = CliRunner()

    result = runner.invoke(cli_frontend, ["requirements"])

    assert "Error: Invalid value for '--manifest'" in result.output

    assert result.exit_code == 2


@freeze_time("2012-10-15 10:00:00")
@pytest.mark.parametrize("manifest_filename", [
    "basic.json",
    "basic.toml",
])
def test_requirements_basic(pytester, caplog, tmp_path, settings, install_structure,
                            manifest_filename):
    """
    With proper manifest values, the command should succeed to run.
    """
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_cwd = Path(td)

        # Install sample structure into temp dir
        install_structure(test_cwd)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / manifest_filename
        manifest_path.write_text(manifest_source.read_text())
        # Append temporary repository path to sys.path during test execution
        pytester.syspathinsert(test_cwd)

        dump_path = test_cwd / "output.txt"

        result = runner.invoke(cli_frontend, [
            "requirements",
            "--manifest", manifest_filename,
            "--repository", "apps_structure",
            "--dump", dump_path,
        ])

        debug_invoke(result, caplog)

        # Get the written dump content
        output = dump_path.read_text().splitlines()

        assert result.exit_code == 0

        assert output == [
            "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
            "# Written on: 2012-10-15T10:00:00",
            "",
            "foo-requirements",
            "bar-requirements",
            "ping-requirements"
        ]

        assert caplog.record_tuples == [
            (
                __pkgname__,
                logging.WARNING,
                "Unable to find module: apps_structure.nope"
            ),
        ]


@pytest.mark.parametrize("manifest_filename", [
    "full.json",
    "full.toml",
])
@freeze_time("2012-10-15 10:00:00")
def test_requirements_full(pytester, caplog, tmp_path, settings, install_structure,
                           manifest_filename):
    """
    With proper manifest value, the command should succeed to run.
    """
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_cwd = Path(td)

        # Install sample structure into temp dir
        install_structure(test_cwd)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / manifest_filename
        manifest_path.write_text(manifest_source.read_text())
        # Load manifest to be able to read some of its values
        manifest = Manifest.load(manifest_path)
        # Copy template from manifest into temp dir
        template_source = settings.fixtures_path / manifest.requirements.template
        template_path = test_cwd / manifest.requirements.template
        template_path.write_text(template_source.read_text())
        # Append temporary repository path to sys.path during test execution
        pytester.syspathinsert(test_cwd)

        dump_path = test_cwd / "full.txt"

        result = runner.invoke(cli_frontend, [
            "requirements",
            "--manifest", manifest_filename,
            "--dump", dump_path,
        ])

        debug_invoke(result, caplog)

        # Get the written dump content
        output = dump_path.read_text().splitlines()

        assert result.exit_code == 0

        assert output == [
            "# Base",
            "Django",
            "",
            "# bar",
            "bar-requirements",
            "",
            "# foo",
            "foo-requirements",
            "",
            "# ping",
            "ping-requirements"
        ]

        assert caplog.record_tuples == [
            (
                __pkgname__,
                logging.WARNING,
                "Unable to find module: apps_structure.nope"
            ),
        ]


@freeze_time("2012-10-15 10:00:00")
def test_requirements_override(pytester, caplog, tmp_path, settings, install_structure):
    """
    Manifest settings should be overrided from CLI arguments if given
    """
    manifest_filename = "full.json"
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_cwd = Path(td)

        # Install sample structure into temp dir
        install_structure(test_cwd)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / manifest_filename
        manifest_path.write_text(manifest_source.read_text())
        # Load manifest to be able to read some of its values
        manifest = Manifest.load(manifest_path)
        # Copy template from manifest into temp dir
        template_source = settings.fixtures_path / manifest.requirements.template
        template_path = test_cwd / "template.txt"
        template_path.write_text(template_source.read_text())
        # Append temporary repository path to sys.path during test execution
        pytester.syspathinsert(test_cwd)

        dump_path = test_cwd / "full.txt"

        result = runner.invoke(cli_frontend, [
            "requirements",
            "--manifest", manifest_filename,
            "--dump", dump_path,
            "--applabel", "// App: {name}\n",
            "--appdivider", "//-\n",
            "--introduction", "// Intro\n",
            "--source", "source.txt",
            "--template", "template.txt",
        ])

        debug_invoke(result, caplog)

        # Get the written dump content
        output = dump_path.read_text().splitlines()

        assert result.exit_code == 0

        assert output == [
            "// Intro",
            "# Base",
            "Django",
            "//-",
            "// App: bar",
            "bar-source",
            "//-",
            "// App: foo",
            "foo-source",
            "//-",
            "// App: ping",
            "ping-source"
        ]

        assert caplog.record_tuples == [
            (
                __pkgname__,
                logging.WARNING,
                "Unable to find module: apps_structure.nope"
            ),
        ]
