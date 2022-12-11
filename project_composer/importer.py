"""
Convenient way to programmatically import a module from a Python path.

"""
import importlib
import sys


def import_module(name, package=None):
    """
    An approximate implementation of import taken from Python importlib documentation.

    This will import a module from given python path in name argument. package argument
    can be given to search in. If module is not in current directory, you will have to
    add its parent path in sys.path. Also relative module path will work only for
    inside a package.

    Arguments:
        name (string): A valid Python path to the module.

    Keyword Arguments:
        package (string): A package name to exclusively search in package tree.

    Returns
        object: Found module object.
    """
    absolute_name = importlib.util.resolve_name(name, package)

    try:
        return sys.modules[absolute_name]
    except KeyError:
        pass

    path = None
    if '.' in absolute_name:
        parent_name, _, child_name = absolute_name.rpartition('.')
        parent_module = import_module(parent_name)
        path = parent_module.__spec__.submodule_search_locations

    for finder in sys.meta_path:
        # Old Meta path finders made for "imp" did not implement the "find_spec" as
        # required with importlib
        if hasattr(finder, "find_spec"):
            spec = finder.find_spec(absolute_name, path)
            # Found module from a loader use it and stop to search
            if spec is not None:
                break
        else:
            continue
    else:
        msg = f'No module named {absolute_name!r}'
        raise ModuleNotFoundError(msg, name=absolute_name)

    module = importlib.util.module_from_spec(spec)
    sys.modules[absolute_name] = module
    spec.loader.exec_module(module)

    if path is not None:
        setattr(parent_module, child_name, module)

    return module
