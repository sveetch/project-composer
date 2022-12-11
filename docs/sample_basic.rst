.. _intro_sample_basic:

============
Basic sample
============

To demonstrate the composition usage we will create a dummy project which should be
able to collect various messages from project applications and print them out in the
expected order.

The final result of this tutorial can be found in its own source repository
`composer-sveetch-python <https://github.com/sveetch/composer-sveetch-python>`_.


Starting project
****************

This document will use virtualenv and pip, although you are free to use your preferred
tools.

First create the project directory where to work: ::

    mkdir composer-sample
    cd composer-sample
    virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install project-composer


Creating project manifest
*************************

The first required step is to create the project manifest to configure how the composer
will work in your project.

.. Note::

    This sample use the TOML file format but it could be also in a JSON file format.

    In fact you could also directly use a Python dictionnary but it would work only
    programatically and you would lose usage of included Composer commandline scripts
    which only works with manifest files.

Open your editor and create a file ``pyproject.toml`` with following content: ::

    [project]
    name = "Sample"

    [tool.project_composer]
    collection = [
        "ping",
        "bar",
        "foo",
    ]
    repository = "application_repository"

For this sample we just focus on the required parameters.


Create application repository
*****************************

As you can see from the manifest, we need a repository directory named
``application_repository`` that will contains application directories ``bar``, ``foo``
and ``ping``.

Finally you will end with the following structure: ::

    application_repository/
    ├── bar/
    │   ├── __init__.py
    │   └── messages.py
    ├── foo/
    │   ├── __init__.py
    │   └── messages.py
    └── ping/
        ├── __init__.py
        └── messages.py

Now enter in the ``application_repository`` directory to create your applications.


The 'foo' application
---------------------

This will be the lowest level application because it does not depend on any other one.

Since it does not have any dependency just create an empty file at
``foo/__init__.py``.

Then we will create the messager part at ``foo/messages.py``: ::

    from project_composer.marker import EnabledApplicationMarker


    class FooFirstMessage(EnabledApplicationMarker):
        def load(self):
            messages = super().load()
            messages.append("Foo first")

            return messages


    class FooSecondMessage(EnabledApplicationMarker):
        def load(self):
            messages = super().load()
            messages.append("Foo second")

            return messages

As you can see, every message classes inherit from ``EnabledApplicationMarker`` which
is just a *marker class*, it does not implement anything and is just used by composer
to recognize the classes it have to register. Any other class without this marker will
be ignored.

So here we created two messager classes, each one implement the ``load()`` method to
append a new message in a list. This method will be used by message collector class to
collect messages from all enabled applications, we will see further about message
collector.

.. Note::

    When there is multiple enabled classes in the same module, they will be collected
    and ordered in the natural order they are defined in their module. Not any
    special sortering is applied.

This is pretty basic but you can implement almost everything you need for your specific
content collector because finally the composer just care about collection, your
final collector will just be a class composed from application classes that you will be
free to use how you need.


The 'bar' application
---------------------

This application will depends on ``foo`` application. In resume for the composer it
will says "'bar' depends from 'foo' so it must be loaded after 'foo'".

Dependency definitions are done in the application base module, so create a file at
``bar/__init__.py`` with this: ::

    DEPENDENCIES = [
        "foo"
    ]

The dependencies are defined in a simple list with their application name. Obviously
a dependency name must exists in your manifest collection since composer must know it
to follow the full dependency tree.

.. Note::

    The order of applications in collection is not really important since composer will
    resolve the right order from dependencies.

    However the order of application dependencies have some influences on final order
    resolving.

Then we will create the messager part at ``bar/messages.py``: ::

    from project_composer.marker import EnabledApplicationMarker


    class BarMessage(EnabledApplicationMarker):
        def load(self):
            messages = super().load()
            messages.append("Bar")

            return messages

This is alike the ``foo`` messager part except it only define a single messager.


The 'ping' application
----------------------

And the last application which is almost identical to ``bar``. It depends from ``bar``
so it inherits from its dependencies and indirectly depends from ``foo``. Composer
will order it after ``foo`` and ``bar``.

Now so create a file at ``ping/__init__.py`` to define its direct dependencies: ::

    DEPENDENCIES = [
        "bar"
    ]

.. Note::

    An application only needs to define its direct dependencies that means only the
    applications it directly requires. When composer perform order resolving will
    walk in dependency dependencies and further, so no need to define the whole
    dependency tree.

Then we will create the messager part at ``ping/messages.py``: ::

    from project_composer.marker import EnabledApplicationMarker


    class PingMessage(EnabledApplicationMarker):
        def load(self):
            messages = super().load()
            messages.append("Ping")

            return messages


Composition usage
*****************

Now that we got the Manifest and the repository, we can start to use composition.

Get back to the parent directory and create a new file at ``hello.py``, everything now
will go in this script file.


Import composition stuff
------------------------

We will start it with the required import from composer and Path object. We need the
composer itself and the used processor to get enabled classes from application message
modules: ::

    from pathlib import Path

    from project_composer.compose import Composer
    from project_composer.processors import ClassProcessor


Messager
--------

To demonstrate the result of composition, we implement a basic message collector,
append this to the script: ::

    class MessagerBase:
        """
        Application messages collector
        """
        def load(self):
            return []

        def get_messages(self):
            output = ""

            messages = self.load()

            output = "\n".join([
                "- Hello {}".format(m) for m in messages
            ])

            return output

As you can see this is something with higher level than composer, it even does not
relate to anything from composer.

This collector will be combined with registered messager classes from applications, it
will be the top of the messager classes hierarchy so its ``load()`` method just setup
a empty list that messager classes will fill each one after ones.

Its ``get_messages()`` method it just a shortand to format the message list. Finally
we just want to output a line starting with ``Hello`` followed by a single message for
each message.


Message processor
-----------------

Now we will create the processor dedicated to find available message classes from
enabled applications, append this to the script: ::

    class MessageProcessor(ClassProcessor):
        """
        Processor for enabled application settings classes for a Django project.
        """
        def get_module_path(self, name):
            """
            Return a Python path for a module name.

            Arguments:
                name (string): Module name.

            Returns:
                string: Python path from repository to application module.
            """
            return "{base}.{part}".format(
                base=self.composer.get_application_base_module_path(name),
                part="messages",
            )

It inherits from ``ClassProcessor`` since this processor only look for Python classes.


.. Note::

    The only purpose of a processor is to find available content like Python classes or
    content files. This is not the goal of a processor to perform anything about
    retrieved content.

    This is because processors are only used by composer to resolve application
    hierarchy and build application parts composition. And so a processor should be
    free of any dependency or related code, excepting the ones from composer.

As you can see in this example the only thing to implement is the ``get_module_path``
method which build the right Python path to search application part modules. Here we
are looking for a ``messages`` module in applications, so for our sample repository it
will match ``foo.messages``, ``bar.messages`` and ``ping.messages`` paths.


Use composed class
------------------

Everything is ready we just have to glue them and get results.

Let's start to initialize the composer: ::

    # Initialize composer with the manifest and the message processor
    _composer = Composer(Path("./pyproject.toml").resolve(),
        processors=[MessageProcessor],
    )

Then proceed to resolve the application order depending their dependencies: ::

    # Resolve dependency order
    _composer.resolve_collection(lazy=False)

And tell the composer to get message classes from enabled applications: ::

    # Search for all enabled message classes
    _classes = _composer.call_processor("MessageProcessor", "export")

At this point the composer is ready, we can start to inspect what's going on.

Let's check the application collection as defined from manifest: ::

    print("collection:", _composer.manifest.collection)

Running the script should return the collection list as defined from manifest, its
order have not changed: ::

    $python hello.py
    collection: ['ping', 'bar', 'foo']

Now add the following code to the script to check for the resolved application list
ordered after dependency hierarchy: ::

    print("apps:", _composer.apps)

Running the script should now output the application list in the right order: ::

    apps: [<AppNode: foo>, <AppNode: bar>, <AppNode: ping>]

As you see the resolved application list is not anymore just name strings but
``AppNode`` objects and most important the order has changed as expected from defined
application dependencies.

And for the last inspection, we will see what message classes have been retrieved from
processor, add the following to the script: ::

    print("_classes:", [cls.__name__ for cls in _classes])

Running the script should now output the class list ordered after the resolved
application order: ::

    _classes: ['FooFirstMessage', 'FooSecondMessage', 'BarMessage', 'PingMessage']

Enough of inspection, we will finish this script. First we build the final messager
class: ::

    # Reverse the list since Python class order is from the last to the first
    _classes.reverse()

    # Add the base messager as the base inheritance
    _COMPOSED_CLASSES = _classes + [MessagerBase]

    # Compose the final messager from found classes
    Messager = type(
        "Messager",
        tuple(_COMPOSED_CLASSES),
        {}
    )

We reverse the class list since Python class inheritance goes from the last to the
first class, then add the ``MessagerBase`` at the end so it is processed first and
finally we build the class with ``type`` using the classes list.

And to finish, we append the lines to exploit this class and print its output: ::

    # Use messager to collect all messages in the right order
    messager = Messager()
    messages = messager.get_messages()

    # And finally output all collected messages
    print()
    print(messages)

Running the script should now output every messages in the right order: ::

    - Hello Foo first
    - Hello Foo second
    - Hello Bar
    - Hello Ping


Conclusion
**********

Because Project composer want to be flexible there is no real shortand to perform
composition in a single line and you will need a little dozen to achieve it.

But there is no magic behind this and you should be able to integrate it everywhere.

Finally this sample is pretty basic and did not mention some advanced features.
