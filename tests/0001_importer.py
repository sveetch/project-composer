import shutil

import pytest

from project_composer.importer import import_module


def test_import_module_success(pytester, settings):
    """
    Ensure import_module is working correctly when search pythonpath is available in
    current 'sys.path'. This uses pytester isolation to avoid import caching issues.

    NOTE:
    The current problem with import_module is that it implies to fully resolve parent
    modules from the pythonpath.
    """
    structure_source_path = settings.fixtures_path / "apps_structure"

    structure_destination_path = pytester.path / "apps_structure"
    pytester.syspathinsert(pytester.path)

    print("structure_source_path:", structure_source_path)
    print("structure_destination_path:", structure_destination_path)

    shutil.copytree(structure_source_path, structure_destination_path)

    mod = import_module("apps_structure.foo.settings")

    print(mod.__name__)

    assert mod is not None
    assert mod.__name__ == "apps_structure.foo.settings"


def test_import_module_fail(pytester, settings):
    """
    import will fail if searched pythonpath is not available in current 'sys.path'

    NOTE:
    The current problem with import_module is that it implies to fully resolve parent
    modules from the pythonpath.
    """
    structure_source_path = settings.fixtures_path / "apps_structure"

    structure_destination_path = pytester.path / "apps_structure"

    print("structure_source_path:", structure_source_path)
    print("structure_destination_path:", structure_destination_path)

    shutil.copytree(structure_source_path, structure_destination_path)

    with pytest.raises(ModuleNotFoundError):
        import_module("apps_structure.foo.settings")
