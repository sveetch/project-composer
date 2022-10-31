.. _intro_overview:

========
Overview
========

What is it ?
************

This is **a set of classes and command lines** to manage project applications.

What we are calling *applications* is just some Python modules but we consider them as
applications from a project. A project application is not treated as a Python package,
however it can come from a package.


Why this system ?
*****************

To correctly **structure project applications parts** and help to manage them.

It is especially useful when creating new projects from a project template where you
predefined many available and applications ready to work that you can enable or not
depending your project needs.


Where it can live ?
*******************

Possibly **in almost any Python project** that need to assemble multiple applications
with multiple parts since it is only involved in composing parts without modifying
application code.

But at first it has been designed to compose a Django project so it is clearly it's
prefered scope.


How does it works ?
*******************

You will **give a project manifest to the composer** that it will use
**to compose applications parts**.

The manifest includes various
parameters but the most important is a list of applications names that we call
*collection*.

These application names are Python module names that have to be available in your
``sys.path``. The composer will walk in these modules to collect their parts like
Django settings, url maps, requirements file, etc.. depending what composer tool you
use.

An application module may describe its dependencies which are other application
names. Dependencies instruct composer to find the right final application order from
the whole collection.

Once collected you can use the applications parts to build some project parts. Like
you can collect every application settings classes to build an unique settings file
correctly ordered.

Composition classes tree
************************

Here for (temporary) technical sample is the involved classes tree when using something
like the ``ComposeDjangoSettings``: ::

    ComposeDjangoSettings
    └── ClassComposer
        └── Composer
            ├── AppStore
            │   └── AppNode
            └── Manifest
                ├── BaseConfig
                │   └── Field classes
                └── RequirementsConfig


* **RequirementsConfig** is a plugin field, that is only used by requirement composer,
  it is always involved but not used except with requirement composer;
* **Fields** are defined in BaseConfig;
* **BaseConfig** is a base for Manifest but only to implement the field management and
  serialization;
* **Manifest** is the highest configuration layer, it implements the way to load manifest
  parameters as config fields. This is the object given to composer to transport
  configuration;
* **AppStore** process application collection defined in manifest to turn each
  application to an **AppNode** then possibly perform dependency resolving and
  ordering. It is only used inside the composer;
* **Composer** implement base methods to process manifest collection and module
  import;
* **ClassComposer** is a common base class to collect Python classes from an
  application module;
* **ComposeDjangoSettings** is currently the highest layer possible, it just implement
  specific composer code on top of ClassComposer;

Here is the wanted new tree: ::

    Composer
    └── ClassComposer inheriters
    ├── AppStore
    │   └── AppNode
    └── Manifest
        ├── BaseConfig
        │   └── Field classes
        └── RequirementsConfig

* **ClassComposer** inheriters (probably to rename) would be some processor classes
  (zero to infinite) that would be looped to work on their specific behaviors using the
  manifest;
* This would benefit to the composer which could run multiple processing task kinds in
  a single instance. Currently we need to start multiple composer instance, each one
  for a processing tasks, it's inefficient;
