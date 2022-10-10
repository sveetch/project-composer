import logging
from pathlib import Path

from click.testing import CliRunner

from project_composer import __pkgname__
from project_composer.cli.entrypoint import cli_frontend


def test_purge_manifest_opt_fail(caplog):
    """
    Command require at least the manifest option and its default value should fail when
    there is not expect manifest file in current working directory.
    """
    runner = CliRunner()

    result = runner.invoke(cli_frontend, ["purge"])

    assert "Error: Invalid value for '--manifest'" in result.output

    assert result.exit_code == 2


def test_purge_commit(pytester, caplog, tmp_path, settings, install_structure):
    """
    With proper manifest value and commit flag enabled, the command should succeed to
    run and perform directories removing.
    """
    manifest_filename = "basic.json"
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_cwd = Path(td)

        # Install sample structure into temp dir
        structure = install_structure(test_cwd)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / manifest_filename
        manifest_path.write_text(manifest_source.read_text())
        # Append temporary repository path to sys.path during test execution
        pytester.syspathinsert(test_cwd)

        result = runner.invoke(cli_frontend, [
            "purge",
            "--manifest", manifest_filename,
            "--repository", "apps_structure",
            "--commit",
        ])

        assert result.exit_code == 0

        remaining_module_dirs = sorted([
            item.name
            for item in structure.iterdir()
            if (item.is_dir() and not item.name.startswith("_"))
        ])

        assert remaining_module_dirs == ["bar", "foo", "ping"]

        assert caplog.record_tuples == [
            (
                __pkgname__,
                logging.INFO,
                "Removing application module: {}/pong".format(structure),
            ),
            (
                __pkgname__,
                logging.INFO,
                "Removing application module: {}/invalid".format(structure),
            ),
            (
                __pkgname__,
                logging.INFO,
                "Removing application module: {}/dummy".format(structure),
            ),
            (
                __pkgname__,
                logging.INFO,
                "Removing application module: {}/empty".format(structure),
            ),
        ]


def test_purge_commit_empty(pytester, caplog, tmp_path, settings, install_structure):
    """
    When everything is enabled and so anything to remove.
    """
    manifest_filename = "full.json"
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_cwd = Path(td)

        # Install sample structure into temp dir
        structure = install_structure(test_cwd)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / manifest_filename
        manifest_path.write_text(manifest_source.read_text())
        # Append temporary repository path to sys.path during test execution
        pytester.syspathinsert(test_cwd)

        result = runner.invoke(cli_frontend, [
            "purge",
            "--manifest", manifest_filename,
            "--repository", "apps_structure",
            "--commit",
        ])

        assert result.exit_code == 0

        remaining_module_dirs = sorted([
            item.name
            for item in structure.iterdir()
            if (item.is_dir() and not item.name.startswith("_"))
        ])

        # Not any application module should have been removed
        assert remaining_module_dirs == [
            "bar", "dummy", "empty", "foo", "invalid", "ping", "pong"
        ]

        assert caplog.record_tuples == [
            (
                __pkgname__,
                logging.WARNING,
                "There was not any application module to remove",
            ),
        ]


def test_purge_export(pytester, caplog, tmp_path, settings, install_structure):
    """
    With proper manifest value and commit flag disabled, the command should succeed to
    run and log info messages about directories to remove.
    """
    manifest_filename = "basic.json"
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_cwd = Path(td)

        # Install sample structure into temp dir
        structure = install_structure(test_cwd)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / manifest_filename
        manifest_path.write_text(manifest_source.read_text())
        # Append temporary repository path to sys.path during test execution
        pytester.syspathinsert(test_cwd)

        result = runner.invoke(cli_frontend, [
            "purge",
            "--manifest", manifest_filename,
            "--repository", "apps_structure",
        ])

        assert result.exit_code == 0

        remaining_module_dirs = sorted([
            item.name
            for item in structure.iterdir()
            if (item.is_dir() and not item.name.startswith("_"))
        ])

        # Not any application module should have been removed
        assert remaining_module_dirs == [
            "bar", "dummy", "empty", "foo", "invalid", "ping", "pong"
        ]

        assert caplog.record_tuples == [
            (
                __pkgname__,
                logging.INFO,
                "This application module would be removed: {}/pong".format(structure),
            ),
            (
                __pkgname__,
                logging.INFO,
                "This application module would be removed: {}/invalid".format(
                    structure
                ),
            ),
            (
                __pkgname__,
                logging.INFO,
                "This application module would be removed: {}/dummy".format(structure),
            ),
            (
                __pkgname__,
                logging.INFO,
                "This application module would be removed: {}/empty".format(structure),
            ),
        ]


def test_purge_export_empty(pytester, caplog, tmp_path, settings, install_structure):
    """
    TODO: When there was not any app module disabled
    """
    manifest_filename = "full.json"
    manifest_source = settings.fixtures_path / "manifests" / manifest_filename

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_cwd = Path(td)

        # Install sample structure into temp dir
        structure = install_structure(test_cwd)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / manifest_filename
        manifest_path.write_text(manifest_source.read_text())
        # Append temporary repository path to sys.path during test execution
        pytester.syspathinsert(test_cwd)

        result = runner.invoke(cli_frontend, [
            "purge",
            "--manifest", manifest_filename,
            "--repository", "apps_structure",
        ])

        assert result.exit_code == 0

        remaining_module_dirs = sorted([
            item.name
            for item in structure.iterdir()
            if (item.is_dir() and not item.name.startswith("_"))
        ])

        # Not any application module should have been removed
        assert remaining_module_dirs == [
            "bar", "dummy", "empty", "foo", "invalid", "ping", "pong"
        ]

        assert caplog.record_tuples == [
            (
                __pkgname__,
                logging.WARNING,
                "There was not any application module to remove",
            ),
        ]
