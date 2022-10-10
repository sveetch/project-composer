import pytest

from project_composer.importer import import_module


def test_import_module_success(pytester, settings, install_structure):
    """
    Ensure import_module is working correctly when search pythonpath is available in
    current 'sys.path'. This uses pytester isolation to avoid import caching issues.
    """
    install_structure(pytester.path)

    pytester.syspathinsert(pytester.path)

    mod = import_module("apps_structure.foo.settings")

    assert mod is not None
    assert mod.__name__ == "apps_structure.foo.settings"


def test_import_module_fail(pytester, settings, install_structure):
    """
    import will fail if searched pythonpath is not available in current 'sys.path'
    """
    install_structure(pytester.path)

    with pytest.raises(ModuleNotFoundError):
        import_module("apps_structure.foo.settings")
