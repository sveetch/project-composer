"""
Pytest fixtures
"""
import shutil

from pathlib import Path

import pytest

import project_composer


pytest_plugins = "pytester"


class FixturesSettingsTestMixin(object):
    """
    A mixin containing settings about application. This is almost only about useful
    paths which may be used in tests.

    Attributes:
        application_path (pathlib.Path): Absolute path to the application directory.
        package_path (pathlib.Path): Absolute path to the package directory.
        tests_dir (pathlib.Path): Directory name which include tests.
        tests_path (pathlib.Path): Absolute path to the tests directory.
        fixtures_dir (pathlib.Path): Directory name which include tests datas.
        fixtures_path (pathlib.Path): Absolute path to the tests datas.
    """
    def __init__(self):
        self.application_path = Path(
            project_composer.__file__
        ).parents[0].resolve()

        self.package_path = self.application_path.parent

        self.tests_dir = "tests"
        self.tests_path = self.package_path / self.tests_dir

        self.fixtures_dir = "data_fixtures"
        self.fixtures_path = self.tests_path / self.fixtures_dir

    def format(self, content):
        """
        Format given string to include some values related to this application.

        Arguments:
            content (str): Content string to format with possible values.

        Returns:
            str: Given string formatted with possible values.
        """
        return content.format(
            HOMEDIR=Path.home(),
            PACKAGE=str(self.package_path),
            APPLICATION=str(self.application_path),
            TESTS=str(self.tests_path),
            FIXTURES=str(self.fixtures_path),
            VERSION=project_composer.__version__,
        )


@pytest.fixture(scope="function")
def temp_builds_dir(tmp_path):
    """
    Prepare a temporary build directory.

    NOTE: You should use directly the "tmp_path" fixture in your tests.
    """
    return tmp_path


@pytest.fixture(scope="module")
def settings():
    """
    Initialize and return settings for tests.

    Example:
        You may use it like: ::

            def test_foo(settings):
                print(settings.package_path)
                print(settings.format("Application version: {VERSION}"))
    """
    return FixturesSettingsTestMixin()


@pytest.fixture(scope="function")
def install_structure(settings):
    """
    Install an apps structure somewhere and clean it from possible Python cache
    dirs.

    Expect argument ``destination`` as a Path object to the directory where to copy the
    source, commonly it should be a temporary path like from Pytest fixture
    ``tmp_path``.

    A keyword argument ``source`` can be given as a Path object to the source to copy
    into destination. If not given, this will use the directory ``apps_structure`` from
    tests data_fixtures.

    Returns Path object to created structure directory.

    Example:
        With usage like this: ::

            def test_foo(install_structure):
                foo = install_structure(
                    Path("/home/foo/bar"),
                    source=Path("/tmp"),
                )

        The ``bar`` directory will be copied into ``/tmp`` and ``foo`` value will be
        ``/tmp/bar``.
    """
    def curry(basepath, source=None):
        source = source or settings.fixtures_path / "apps_structure"
        destination = basepath / source.name
        shutil.copytree(source, destination)

        for p in destination.rglob("__pycache__"):
            shutil.rmtree(p)

        return destination

    return curry
