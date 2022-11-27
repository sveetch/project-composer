.. _intro_history:

=======
History
=======

Version 0.7.0 - Unreleased
--------------------------

* TODO: Fix RTD build, pin python build to the right one, currently rtd return error: ::

    Configuration error:
    There is a programmable error in your configuration file:

    Traceback (most recent call last):
    File "/home/docs/checkouts/readthedocs.org/user_builds/project-composer/envs/latest/lib/python3.6/site-packages/sphinx/config.py", line 350, in eval_config_file
        exec(code, namespace)
    File "/home/docs/checkouts/readthedocs.org/user_builds/project-composer/checkouts/latest/docs/conf.py", line 15, in <module>
        from project_composer import __version__ as project_composer_version
    File "/home/docs/checkouts/readthedocs.org/user_builds/project-composer/envs/latest/lib/python3.6/site-packages/project_composer/__init__.py", line 2, in <module>
        from importlib.metadata import version
    ModuleNotFoundError: No module named 'importlib.metadata'

* Improve documentation and release it to *Read the documentation* site;
* ONDOING: Added new "check" method to composer and processors to display output
  debugging about project composition;
* Moved all Django related stuff to contrib.django;


Version 0.6.0 - 2022/11/02
--------------------------

**Refactoring which bring backward incompatible changes**

* Refactored composer layer to use sub processors for part kinds (classes, django,
  text, etc..) so an unique composer instance can process multiple parts and this is
  more efficient that using a new composer for each part;
* Fixed resolving issues with application order resolving, Composer inheriter and
  ``_MODULE_PYTHONPATH`` (that have be renamed to ``_APPLICATION_MODULE_PYTHONPATH``);
* Composer do not execute its ``resolve_collection`` method on init, it needs to be
  called explicitely after, resulting in its attribute ``apps`` to be empty on init;
* Added ``lazy`` option to ``Composer.resolve_collection()`` method to enforce
  lazy ordering even if the manifest attribute ``no_ordering`` is disabled;


Version 0.5.0 - 2022/10/31
--------------------------

**New features and refactoring which bring backward incompatible changes**

* Implemented application order scheduling with ``DEPENDENCIES`` and ``PUSH_END``
  variables within application base module (``__init__.py``);
* ``Manifest.apps`` has been renamed to ``Manifest.collection``;
* Added manifest field ``default_store_app`` to set a default application name to add
  to applications without any dependency;
* Added manifest field ``default_store_app`` to disable ordering resolution;
* Fixed tests so every ones that performed structure sample importation are running
  into a temporary directory, not anymore importing on structures from "data_fixtures";


Version 0.4.2 - 2022/10/16
--------------------------

* Changed default manifest filename to ``pyproject.toml``;
* Changed commandlines so they automatically and correctly manage command arguments to
  override manifest arguments;


Version 0.4.1 - 2022/10/16
--------------------------

This release ensure any settings can be managed from Manifest and that commandlines
can override Manifest settings.


Version 0.4.0 - 2022/10/15
--------------------------

**New Manifest system bring backward incompatible changes**

* Fixed Makefile install since colorlog is no longer an optional dependency;
* Update tox config to remove colorlog switch and to avoid installing documentation and
  release stuff;
* Added Manifest model to store manifest datas;
* Added ``tomli`` dependency to add TOML format support for manifest;
* Requirements settings are now a part of manifest;
* Composer classes no longer accept options from args or kwargs, everything is driven
  by Manifest. However commandlines are able to override manifest options from
  arguments;
* RequirementsComposer have been removed since it has no meaning anymore, the
  'requirements' commandline just directly use TextContentComposer;


Version 0.3.0 - 2022/10/11
--------------------------

* Move CLI to click instead of argparse;
* Renamed option ``--appsdir`` to ``--repository``;
* Renamed option ``--base`` to ``--template``;
* Splitted CLI in subcommands, no longer need of ``--mode`` option;
* Improved some test to be safer with importation;
* Added ``purge`` command to definitively remove application module directory from
  repository that are not enabled in manifest;


Version 0.2.3 - 2022/10/05
--------------------------

* Fixed missing syspath argument usage from CLI;
* Fixed requirements dump from CLI;


Version 0.2.2 - 2022/10/05
--------------------------

* Fixed collector for some issues to work correctly;


Version 0.2.1 - 2022/10/04
--------------------------

* Fixed importer for some packages which add a Meta path finder in the old way (like for
  deprecated ``imp``);
* Added a new test around importer;
* Removed some forgotten print usage from code;


Version 0.2.0 - 2022/10/02
--------------------------

* Moved package __init__ to importlib instead of setuptools stuff;
* Made the colorlog dependancy optional so by default the package has not any
  dependancy;
* Added basic commandline with 'version' and 'requirements' modes for now;


Version 0.1.0 - 2022/10/02
--------------------------

*Not published to Pypi*

First commit with working stuff and initial composers. Still needs a CLI.
