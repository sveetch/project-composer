import logging
from pathlib import Path

from click.testing import CliRunner

from freezegun import freeze_time

from project_composer import __pkgname__
from project_composer.cli.entrypoint import cli_frontend


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
def test_requirements_basic(pytester, caplog, tmp_path, settings, install_structure):
    """
    With proper manifest value, the command should succeed to run.
    """
    manifest_source = settings.fixtures_path / "manifests" / "basic.json"

    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        test_cwd = Path(td)

        # Install sample structure into temp dir
        install_structure(test_cwd)
        # Copy manifest sample into temp dir
        manifest_path = test_cwd / "basic.json"
        manifest_path.write_text(manifest_source.read_text())
        # Append temporary repository path to sys.path during test execution
        pytester.syspathinsert(test_cwd)

        dump_path = test_cwd / "output.txt"

        result = runner.invoke(cli_frontend, [
            "requirements",
            "--manifest", "basic.json",
            "--repository", "apps_structure",
            "--dump", dump_path,
        ])

        # Get the written dump content
        output = dump_path.read_text().splitlines()

        # print("=> result.output <=")
        # print(result.output)
        # print()
        # print("=> caplog.record_tuples <=")
        # print(caplog.record_tuples)
        # print()
        # print("=> result.exception <=")
        # print(result.exception)
        # if result.exception:
        #     raise result.exception

        assert result.exit_code == 0

        assert output == [
            "# This file is automatically overwritten by composer, DO NOT EDIT IT.",
            "# Written on: 2012-10-15T10:00:00",
            "",
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

        assert caplog.record_tuples == [
            (
                __pkgname__,
                logging.WARNING,
                "Unable to find module: apps_structure.nope"
            ),
        ]
