.. _intro_history:

=======
History
=======

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
