========================================
Django Object Log
========================================

This app provides the ability to log user actions on model instances. Action
types can be defined by app developers, and can reference multiple objects.
Each action type defines it's own template used for rendering output of the
message. It allows verbose messages specific to the action that occurred.

Object Log includes shortcuts both for adding entries and building views to
display them.


Installation
----------------------------------------

There are several ways to install Object Log.

Object Log ships a standard distutils ``setup.py``. A classic invocation
to install from setup.py might be:

.. code-block:: console

    $ python setup.py install

You may need to add sudo in order to install to the system Python.

.. code-block:: console

    $ sudo python setup.py install

We also have Object Log on PyPI, so it can be installed using pip.
(``easy_install`` also works, but we do not recommend it.)

.. code-block:: console

    $ pip install django-object-log

If you are installing Object Log directly into a Django app, and want
to distribute Object Log with your app, simply copy the
object_log folder into your Django project.


Configuring Your Django Project
----------------------------------------

1. Add "object_log" to ``INSTALLED_APPS``.
2. Run ``./manage.py syncdb``.
3. Add ``object_log.urls`` to your site's urls if you wish to add views for
   displaying logs.


Using Object Log
----------------------------------------

First, register some action types.  This can be done at any time but should
ideally be done once in ``models.py``.  ``LogActions`` require both a key and a
template used to render that Action type.

.. code-block:: pycon

    >>> from object_log.models import LogAction
    >>> LogAction.objects.register('MY_ACTION', 'path/to/my/template.html')

Now, that LogAction type can be used whenever that action occurs

.. code-block:: pycon

    >>> from object_log.models import LogItem
    >>> log = LogItem.objects.log_action
    >>> log('MY_ACTION', user, some_object)
    >>> log('EDIT', user, some_object)
    >>> log('DELETE', user, some_object)

Arbitrary data can also be included with each log entry by including a
dict  It is available in the LogAction template as {{data}}.  This is
useful for caching information to reduce related queries when rendering
logs

.. code-block:: pycon

    >>> log('MY_ACTION', user, {'my_obj':str(obj1})

The data dict can be automatically populated from objects using a cache
function registered with the LogAction.  The cache function recieves the user,
objects, and any data passed to log_Action().  It should return a dict.  This
data overwrites manual data, you must merge it manually if you want to use both.

.. code-block:: pycon

    >>> def cache(user, obj1, obj2, obj3, data):
    >>>    return dict(obj_str=str(obj1))
    >>>
    >>> LogAction.objects.register('MY_ACTION', 'path/to/my/template.html', cache)

log_action can then be used as normal.

.. code-block:: pycon

    >>> log('MY_ACTION', user, some_object)


See the `wiki <http://code.osuosl.org/projects/django-object-log/wiki>`_ for
more details.


Authors
-------

Object Log was implemented at the Oregon State University Open Source Lab
(`OSUOSL <https://code.osuosl.org/>`_).  The primary author was Peter Krenesky.
