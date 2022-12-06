.. _intro_manifest:

========
Manifest
========

A manifest contains everything to describe how the composer will behaves.

You can supply a manifest either as a JSON file or a TOML file. And if needed,
also as a Python dictionnary but it won't work for the command line interface.

Composer does not write anything in a manifest file.


Fields
******

name
    Just a label for the project, this is almost never used from code, it's purpose
    is mostly about to identify your configuration. However it is required.
collection
    This is a required field to list the names of enabled application modules to enable
    in your project. These applications must exists in the application repository.

    Obviously these application names must be valid Python module names.
repository
    A required field to define the module where belong your applications. It must be
    available from your ``sys.path``.
syspaths
    An optionnal list for some paths to load in your ``sys.path``. This may be useful
    if your repository is not already available from your current ``sys.path``.

    The list is empty on default.

    The composer automatically loads these paths during its initialization.
default_store_app
    Optionnal application name to add as a dependency on applications which don't have
    any dependency yet. This may be useful to force regrouping under a single
    application to enforce an unique main hierarchy.

    There is no default dependency on default.
no_ordering
    Optionnal boolean to disable (if true) application order resolving, then the
    resolver from compose will just return the application in their natural order as
    defined from manifest collection.

    This is false on default, the resolving is always enabled.


Requirements plugin fields
--------------------------

This is a plugin configuration dedicated to the command ``requirements``, it is
totally optionnal especially if you don't plan to use this command.

source_filename
    A filename to search for in application modules to get application requirements.
    Each founded file will be added to the project requirements in the final
    requirements file.

    This is ``requirements.txt`` on default.
template
    A relative path to a text file used to start the final requirement file. It must be
    valid with the requirements file syntax.

    You can use it to add some requirements which are not involved by project
    applications.

    It is empty on default.
application_label
    A string to add just before the requirements from an application. Empty on default.
application_divider
    A string to add between two applications requirements blocks. Empty on default.
introduction
    A string to add before everything (possible template and all requirements) which
    accept a pattern ``{creation_date}`` where to put the file creation date.

    If you don't want an introduction, set this to ``false`` or an empty string.

    On default this is: ::

        # This file is automatically overwritten by composer, DO NOT EDIT IT.\n
        # Written on: {creation_date}\n\n


Manifest as JSON
****************

The JSON format structure is : ::

    {
        "name": "Project name",
        "collection": [
            "bar"
        ],
        "repository": "application_repository",
        "syspaths": [],
        "default_store_app": "foo_app",
        "no_ordering": false,
        "requirements": {
            "source_filename": "requirements.txt",
            "template": "requirements_template.txt",
            "application_label": "# {name}\n",
            "application_divider": "\n",
            "introduction": "# Written on: {creation_date}\n"
        }
    }


Manifest as TOML
****************

The TOML format structure is : ::

    [project]
    name = "Project name"

    [tool.project_composer]
    name = "Project name custom"
    collection = [
        "bar",
    ]
    repository = "application_repository"
    syspaths = []
    default_store_app = "foo_app"
    no_ordering = false

    [tool.project_composer.requirements]
    source_filename = "requirements.txt"
    template = "requirements_template.txt"
    application_label = "# {name}\n"
    application_divider = "\n"
    introduction = "# Written on: {creation_date}\n"

.. Note::

    You probably noticed there is two ``name`` options from different sections.

    The one from ``tool.project_composer`` section is the first one checked and the
    second one from ``project`` is used as a fallback. This is because the
    ``pyproject.toml`` format require the ``project.name`` option so you should already
    have a project name but you are able to define a custom one if needed.


Manifest as Python dictionnary
******************************

The dictionnary format structure is identical to the JSON one.
