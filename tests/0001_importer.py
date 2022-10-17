import pytest

from project_composer.importer import import_module


def test_import_module_success(pytester, settings, basic_structure):
    """
    Ensure import_module is working correctly when search pythonpath is available in
    current 'sys.path'. This uses pytester isolation to avoid import caching issues.
    """
    basic_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    mod = import_module("basic_structure.foo.settings")

    assert mod is not None
    assert mod.__name__ == "basic_structure.foo.settings"


def test_import_module_fail(pytester, settings, basic_structure):
    """
    import will fail if searched pythonpath is not available in current 'sys.path'
    """
    basic_structure(pytester.path)

    with pytest.raises(ModuleNotFoundError):
        import_module("basic_structure.foo.settings")
