.. _intro_cli:

============
Command line
============

Usage
-----

You may reach the tool either directly: ::

        .venv/bin/project_composer

Or more simplier after environment have been activated: ::

    source .venv/bin/activate
    project_composer


Help
----

There is the base tool help: ::

    project_composer -h

This list base options and available tasks.

Then each command have its own options you can see within its help: ::

    project_composer [TASK] -h


Requirements
------------

Since application requirements are stored in simple text files, there is no need to
implement any code to build composed requirement for a project. This command is able to
collect applications requirements and to output composition or writing them to a
file: ::

    project_composer requirements

Obviously you will need a project manifest for composer configuration. If no manifest
argument is given, the default behavior is to search for a file ``pyproject.toml`` in
your current directory to get the composer manifest.

Finally, many manifest options can be overriden from command argument, see help for
more details.

.. Note::

    This command have its own dedicated configuration defined as a manifest plugin,
    see the Manifest documentation for the **Requirements plugin fields** for more
    details.


Purge
-----

Since application repository is something to be shared among many projects, it can
contains a lot of applications that won't never be used anymore when the project has
reached a final stage.

For this purpose you may want to clean repository for unused applications. The purge
command can help for this: ::

    project_composer purge

This will scan repository for any application that is not enabled from manifest and
remove it. This is definitive, so this command should be used with caution.

