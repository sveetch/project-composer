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
predefined many available applications ready to work that you can enable or not
depending your project needs.


Where it can live ?
*******************

Possibly **in almost any Python project** that need to assemble multiple applications
with multiple parts. And since it is only involved in composing parts without modifying
application code, it should not have any real impact on project code.

Historically it has been designed to compose a Django project so this is clearly it's
best scope.


How does it works ?
*******************

You will **give it a project manifest** that will be used **to compose applications
parts**.

The **manifest includes** various parameters but the most important is **a list of
applications names** (called *collection*) **and the application repository** path (as
a Python path like ``foo.bar``).

These application names are Python module names that have to be available in your
application repository. The composer will walk in these modules to collect their parts
like classes, content file, etc.. depending composer processors.

An application module may describe its dependencies. Dependencies instruct composer to
resolve the right final application order from the whole collection.

Once collected you can use the applications parts to build some project parts.


Practical usage
***************

The most obvious use case is a Django project:

* You can use a processor to compose your settings;
* A processor to compose your urls;
* And finally a processor to compose your project requirements;

All of these parts would be defined in each application like Django builtins, a CMS,
a blog, etc.. from the application repository. Resulting in something like
this: ::

    application_repository/
    ├── blog/
    │   ├── __init__.py
    │   ├── requirements.txt
    │   ├── settings.py
    │   └── urls.py
    │
    ├── cms/
    │   ├── __init__.py
    │   ├── requirements.txt
    │   ├── settings.py
    │   └── urls.py
    │
    └── django/
        ├── __init__.py
        ├── requirements.txt
        ├── settings.py
        └── urls.py

.. Note::

    Composer is not tied to any kind of part. Previous example was about Django
    settings, urls and requirements but you can create processor for anything, easily
    with builtin Python classes and text content files processors or on your own for
    anything else.

    Not any part is required from application so an application may not have a
    settings file or any other part, the composer won't break.

    However any Python part must be a valid module since it is imported.

Benefits
--------

The application repository can be maintained once and shared to each new project and
everything is ready to work.

Also this is a good way to structure a project with a proper separation of concerns.


Involved composer classes path
******************************

Still there ?

Let's dig a little more in technical layer, here is the involved classes hierarchy
when using composer: ::

    Composer
    ├── Manifest
    │   └── BaseConfig
    │   │   └── Fields
    │   └── BasePluginConfig
    ├── AppStore
    │   └── AppNode
    └── Processors

Composer
    The class you will use to open a manifest, define some processors, execute them
    and make parts compositions.
Manifest
    The loaded manifest where belong composition configuration.
BaseConfig
    The class which manage all configuration options from fields.
Fields
    A field define some parameters for a configuration option, stored as a configuration
    attribute. There is multiple fields, each one for a specific Python type (string,
    list, etc..). Fields are use to validate given option values.
BasePluginConfig
    Optional application part that need specific configuration options can be defined
    as a plugin.
AppStore
    This where the composer will store collected applications and get the resolved
    application in order to their dependencies.
AppNode
    The class to represent an application in the store.
Processors
    A processor expose some methods to perform jobs on an application part. A processor
    should always be dedicated to a specific part.

.. admonition:: In resume

    #. Composer open and read given manifest;
    #. Use the collection to scan repository applications for their defined dependencies;
    #. Then resolve the application order implied by dependencies and return the
       application list in the right order.

    In common usage, you will just have to make a manifest file, load it with
    composer and enable some processors. You won't really have to care about other
    classes like ``AppNode``, ``AppStore``, etc..
