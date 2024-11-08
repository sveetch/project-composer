
=========
Changelog
=========

Version 0.7.2 - 2024/11/04
**************************

**This is only a minor release to enhance development environment**

* Added support for Python 3.11;
* Added minimal version for all requirements;
* Updated configuration for RTD build;
* Updated Makefile for minor enhancements;
* Updated "development" documentation for a note about Graphviz requirement to build
  doc diagrams;
* Updated script to freeze local dependencies;


Version 0.7.1 - 2023/08/19
**************************

* Updated Makefile to use ANSI color on task titles;
* Fixed package setup to not install Tox with dev extra requirements;
* Limited Tox suites to minimal and maximal supported Python version to speed up
  quality validation;
* Moved documentation theme to "Furo";
* Added a logo for this project;


Version 0.7.0 - 2022/12/12
**************************

* Improved documentation and release it to *Read the documentation* site;
* Built some diagrams for documentation with
  `diagrams package <https://github.com/mingrammer/diagrams>`_, a distinct makefile
  command ``diagrams`` has been added to build them into documentation static file
  directory;
* Added new "check" method to composer and processors to display output debugging about
  project composition;
* Moved all Django related stuff to contrib.django;
* Fixed RTD configuration to use Python3.8 to fix building;
* Changed ``Composer.find_app_module`` so it only emits ``log.debug`` instead of
  ``log.warning`` when it does not find a module;


Version 0.6.0 - 2022/11/02
**************************

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
**************************

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
**************************

* Changed default manifest filename to ``pyproject.toml``;
* Changed commandlines so they automatically and correctly manage command arguments to
  override manifest arguments;


Version 0.4.1 - 2022/10/16
**************************

This release ensure any settings can be managed from Manifest and that commandlines
can override Manifest settings.


Version 0.4.0 - 2022/10/15
**************************

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
**************************

* Move CLI to click instead of argparse;
* Renamed option ``--appsdir`` to ``--repository``;
* Renamed option ``--base`` to ``--template``;
* Splitted CLI in subcommands, no longer need of ``--mode`` option;
* Improved some test to be safer with importation;
* Added ``purge`` command to definitively remove application module directory from
  repository that are not enabled in manifest;


Version 0.2.3 - 2022/10/05
**************************

* Fixed missing syspath argument usage from CLI;
* Fixed requirements dump from CLI;


Version 0.2.2 - 2022/10/05
**************************

* Fixed collector for some issues to work correctly;


Version 0.2.1 - 2022/10/04
**************************

* Fixed importer for some packages which add a Meta path finder in the old way (like for
  deprecated ``imp``);
* Added a new test around importer;
* Removed some forgotten print usage from code;


Version 0.2.0 - 2022/10/02
**************************
* Moved package __init__ to importlib instead of setuptools stuff;
* Made the colorlog dependancy optional so by default the package has not any
  dependancy;
* Added basic commandline with 'version' and 'requirements' modes for now;


Version 0.1.0 - 2022/10/02
**************************

*Not published to Pypi*

First commit with working stuff and initial composers. Still needs a CLI.
