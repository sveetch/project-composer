.. _intro_workflow:

========
Workflow
========


Application resolving
*********************

Basically the composer is driven by the manifest which defines behavior options and
especially the application repository to use. Once manifest have been consumed, the
composer can resolve application from repository.

.. figure:: /_static/resolver.png
   :align: center

   The resolver put in order applications from repository depending from their
   dependencies, then store them internally as AppNode objects into Application store.


.. Note::

    By resolving, we mean "put in order" applications depending their dependencies. This
    means the application collection order defined in manifest is secondary and dependency
    is more important to compute final order.

Also a special option "Push end" can be used to force some application to be pushed
after every other application that do not use this option.


Part processors
***************

Processors are enabled on composer initialization, then project can call for a
processor method to collect its part from application classes and build a composed part
that project can use.

.. figure:: /_static/processors.png
   :align: center

   Each invoked processor will scan applications from store to find their elligible
   classes that will compose the project parts.

Commonly, a processor is dedicated to an unique project part and so a it have
a standardized method ``export()`` to go collecting applications classes for a single
part kind.

Also, a processor have a ``check()`` method which output debug informations about
processing enabled applications.


Composer workflow
*****************

Manifest consumption and processor activations are made during composer initialization,
then the resolver can be called to build application store and finally the processor
methods can be executed to proceed to project parts compositions.

.. figure:: /_static/workflow.png
   :align: center

   The complete composer workflow involves everything from the application repository
   to the final project parts.

Practical situation with Django
*******************************

With a Django project, we can see how composer can help to manage project parts.

.. figure:: /_static/django.png
   :align: center

   Resumed workflow for a Django project.
