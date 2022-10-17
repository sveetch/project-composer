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
