"""
.. NOTE:
    As requirements commandline is the only one to implement every possible manifest
    settings and CLI arguments, these tests also make global coverage against CLI and
    its manifest usage.
"""
import shutil
import sys
from pathlib import Path

import pytest

from click.testing import CliRunner

from freezegun import freeze_time

from project_composer.cli.entrypoint import cli_frontend
# from project_composer.utils.tests import debug_invoke
from project_composer.manifest import Manifest
from project_composer.compose import Composer


def test_requirements_manifest_opt_fail():
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
def test_requirements_basic(pytester, caplog, tmp_path, settings, basic_structure,
                            manifest_filename):
    """
    With proper manifest values, the command should succeed to run.
    """
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_cwd = Path(td)

        # Install sample structure into temp dir
        basic_structure(test_cwd)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / manifest_filename
        shutil.copyfile(manifest_source, manifest_path)
        # Append temporary repository path to sys.path during test execution
        pytester.syspathinsert(test_cwd)

        dump_path = test_cwd / "output.txt"

        result = runner.invoke(cli_frontend, [
            "requirements",
            "--manifest", manifest_filename,
            "--repository", "basic_structure",
            "--dump", dump_path,
        ])

        # debug_invoke(result, caplog)

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

        assert caplog.record_tuples == []


def mocked_composer_set_syspaths(pytester_instance):
    """
    A function to use to mockup the BaseComposer.set_syspaths to pytester.syspathinsert

    This return a curried function that have been given the pytester instance.
    """
    def curry(obj, paths):
        for path in paths:
            if path not in sys.path:
                pytester_instance.syspathinsert(path)

    return curry


@pytest.mark.parametrize("manifest_filename", [
    "full.json",
    "full.toml",
])
@freeze_time("2012-10-15 10:00:00")
def test_requirements_full(monkeypatch, pytester, caplog, tmp_path, settings,
                           basic_structure, manifest_filename):
    """
    With proper manifest value, the command should succeed to run.
    """
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        # Enforce composer to use pytester.syspathinsert
        monkeypatch.setattr(
            Composer,
            "set_syspaths",
            mocked_composer_set_syspaths(pytester)
        )

        test_cwd = Path(td)

        # Full manifest use a container directory for the repository so we can test
        # about syspath but it does not exists from structure so we create it on the fly
        container = test_cwd / "container"
        container.mkdir(mode=0o777)

        # Install sample structure into temp dir
        basic_structure(container)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / manifest_filename
        shutil.copyfile(manifest_source, manifest_path)
        # Load manifest to be able to read some of its values
        manifest = Manifest.load(manifest_path)
        # Copy template from manifest into temp dir
        template_path = test_cwd / manifest.requirements.template
        shutil.copyfile(
            settings.fixtures_path / manifest.requirements.template,
            template_path
        )

        dump_path = test_cwd / "full.txt"

        result = runner.invoke(cli_frontend, [
            "requirements",
            "--manifest", manifest_filename,
            "--dump", dump_path,
        ])
        # debug_invoke(result, caplog)

        # Get the written dump content
        output = dump_path.read_text().splitlines()

        assert result.exit_code == 0

        assert output == [
            "# Base",
            "Django",
            "",
            "# foo",
            "foo-requirements",
            "",
            "# bar",
            "bar-requirements",
            "",
            "# ping",
            "ping-requirements"
        ]

        assert caplog.record_tuples == []


@freeze_time("2012-10-15 10:00:00")
def test_requirements_override(monkeypatch, pytester, caplog, tmp_path, settings,
                               basic_structure):
    """
    Manifest settings should be overrided from CLI arguments if given
    """
    manifest_filename = "full.json"
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        # Enforce composer to use pytester.syspathinsert
        monkeypatch.setattr(
            Composer,
            "set_syspaths",
            mocked_composer_set_syspaths(pytester)
        )

        test_cwd = Path(td)

        # This test use a different path to the repository so we can test overriding
        # manifest syspaths but it does not exists from structure so we create it on
        # the fly
        container = test_cwd / "override"
        container.mkdir(mode=0o777)

        # Install sample structure into temp dir
        structure = basic_structure(container)
        # Rename repository dir to test overriding manifest repository from CLI args
        new_repository = container / "new_repository"
        structure.rename(new_repository)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / manifest_filename
        shutil.copyfile(manifest_source, manifest_path)
        # Load manifest to be able to read some of its values
        manifest = Manifest.load(manifest_path)
        # Copy template from manifest into temp dir
        template_path = test_cwd / "template.txt"
        shutil.copyfile(
            settings.fixtures_path / manifest.requirements.template,
            template_path
        )

        dump_path = test_cwd / "full.txt"

        result = runner.invoke(cli_frontend, [
            "requirements",
            "--manifest", manifest_filename,
            "--syspath", str(container),
            "--repository", "new_repository",
            "--dump", dump_path,
            "--applabel", "// App: {name}\n",
            "--appdivider", "//-\n",
            "--introduction", "// Intro\n",
            "--source", "source.txt",
            "--template", "template.txt",
        ])

        # debug_invoke(result, caplog)

        # Get the written dump content
        output = dump_path.read_text().splitlines()

        assert result.exit_code == 0

        assert output == [
            "// Intro",
            "# Base",
            "Django",
            "//-",
            "// App: foo",
            "foo-source",
            "//-",
            "// App: bar",
            "bar-source",
            "//-",
            "// App: ping",
            "ping-source"
        ]

        assert caplog.record_tuples == []
