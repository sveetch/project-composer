.. _intro_history:

=======
History
=======

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
