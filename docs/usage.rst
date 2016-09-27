Usage
=====


Registering action types
------------------------

Message types must be registered with Object Log as a ``LogAction`` before they
can be used.  This informs Object Log about what information you will be
logging and how to render it.  ``LogAction`` is comprised of a key and a Django
template.  The key will be used to identify the type quickly by developers.

.. code-block:: python

    from object_log.models import LogAction
    LogAction.objects.register('MY_EVENT','path/to/my/template.html')

Registering a ``LogAction`` for second time will override the existing
settings.  This allows you to replace the template used to render an action
type provided by another app.


Adding log entries
------------------

LogItem can be created manually, but the prefered method for adding log
entries is to use :func:`object_log.models.LogItem.objects.log_action`, which
uses an internal cache provided by LogAction to avoid queries to fetch
``LogAction`` from the database.

.. function:: object_log.models.LogItem.objects.log_action(key, user, object1, object2=None, object3=None, data=None)

    Creates new log entry

    :param key: the key corresponding to the ``LogAction`` you are recording
    :type key: str
    :param user: the user performing the action
    :param object1..object3: the objects involved in the action.  They
                             are stored using a ``GenericForeignKey``.  At
                             least one object is required
    :param data: arbitrary data that can be stored with a log entry
    :type data: JSON-serializable dict


.. _arbitrary_data:

Arbitrary data
~~~~~~~~~~~~~~

Arbitrary data can be stored within log entry.  For instance you may want to
store a list of properties that were edited.  Storing arbitrary data allows
``log_items`` to be rendered quickly without the need to look up related
objects.

Arbitrary data is added by including the ``data`` keyword argument when calling
``log_action``.  Data should be a dict containing values that are JSON
serializable.

The data is serialized automatically with ``json`` and is available within
templates as ``log_item.data``.

Sample usage:

.. code-block:: python

    from object_log.models import LogItem

    # store log_action for faster access
    LOG = LogItem.objects.log_action

    def show_model(request, pk):
        "Example view that retrieves an object by its PK."
        obj = SomeModel.objects.get(pk=pk)
        LOG('MODEL_VIEWED', request.user, obj, data={'model_data': obj.data})


Caching
~~~~~~~

In addition manually specifying data, a cache function can be used to
automatically build cached data.  Cache functions are declared when registering
the ``LogAction``.  The function is used to parse related data from a log
entry.

* The function should accept ``user``, ``object1``, ``object2``, ``object3``,
  and ``data`` arguments.
* The function should return a **dict**.
* The function should be flexible enough to handle when any object is ``None``.

Arbitrary data can still be supplied but cached data will take precedence.

Sample usage:

.. code-block:: python

    from object_log.models import LogAction

    def build_cache(user, obj1, obj2, obj3, data):
        return {'foo': obj1.foo}

    LogAction.objects.register('MY_EVENT', 'template.html', build_cache)

If you make changes to a cache, the cache should be rebuilt using ``manage.py
rebuild_log_cache``.  This is a naive rebuild which will add cached values to
existing data.  If cache changes in more substantial ways you will be required
to create a manual migration script.


Creating templates for action types
-----------------------------------

Each ``LogAction`` must have a template registered to render it:

.. code-block:: django

    {# sample template for MY_EVENT #}
    did something interesting to

Templates tags and filters can be used like in any other Django template.  You
may also use contextual links to improve navigation:

.. code-block:: django

    <a href="{% url user-detail log_item.user_id %}">{{log_item.user.username}}</a>
    did something interesting to
    <a href="{% url object-detail log_item.object1_id %}">{{log_item.object1}}</a>

**Timestamp** should not be output in the log.  The default template for
rendering log entries outputs the timestamp so that it is consistent across
all log types.

Related objects
---------------

Log entries are not deleted with their related objects.  This is a business
logic decision left up to projects that use Object Log.

When related objects are deleted they are returned as a ``None`` within the
template.  This will result in either an empty space, or an exception if you
applied a template filter incapable of handling an ``None`` for it input.

:ref:`Arbitrary data <arbitrary_data>` can be used to store values that will
persist beyond the deletion of an object.


Built-in action types
---------------------

``CREATE``, ``EDIT``, ``DELETE`` are registered by default since these actions
occur in nearly every Django app.  The supplied templates are basic and do not
provide contextually links to the objects.


Displaying logs
---------------

Object Log provides some generic views for rendering a log for either ``User``
or for a related object.

Activate them by adding ``object_log.urls`` to your project's ``urls.py``:

.. code-block:: python

    urlpatterns += patterns('',
        (r'^', include('object_log.urls')),
    )

Generic views:

.. autofunction:: object_log.views.list_user_actions(request, pk)
.. autofunction:: object_log.views.list_for_user(request, pk)
.. autofunction:: object_log.views.list_for_group(request, pk)
.. autofunction:: object_log.views.list_for_object(request, obj)

Sample usage of :func:`object_log.views.list_for_object`:

.. code-block:: python

    from object_log.views import list_for_object

    def list_for_my_model(request, pk):
        """ example view using list_for_object to display a log """
        obj = MyModel.objects.get(pk=pk)
        return list_for_object(request, obj)

:func:`object_log.views.list_for_object` performs no permission checks.  It is
impossible to determine the permission requirements of your project.  It is up
to you to implement required security.  Here's a little example, though:

.. code-block:: python

    from django.contrib.auth.decorators import login_required
    from django.http import HttpResponseForbidden

    from object_log.views import list_for_object

    @login_required
    def list_for_my_model(request, pk):
        """ example view using list_for_object to display a log """
        obj = MyModel.objects.get(pk=pk)
        if request.user.has_perm('MyModel.my_perm'):
            return list_for_object(request, obj)
        else:
            return HttpResponseForbidden("Insufficient permissions!")


Custom view
-----------

If you need more customization, such as being able to filter the list of log
entries you can create a custom view.  The generic views all use
``object_log/log.html`` to render a list of ``LogItem``.

.. code-block:: python

    from object_log.models import LogItem

    def custom_log_output(request):
        log = LogItem.objects.filter(q).distinct()

        return render_to_response('object_log/log.html',
            {'log': log},
            context_instance=RequestContext(request))

Additional context can be passed to all ``LogItem`` by included ``context`` in
the ``Context`` used to render ``object_log/log.html``:

.. code-block:: python

    def custom_log_output(request):
        # ...
        return render_to_response('object_log/log.html',
            {'log': log
             'context': {'user': request.user}
            }, context_instance=RequestContext(request))
