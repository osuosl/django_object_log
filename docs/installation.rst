Installation
============

To install Django Object Log, simply pull it from PyPI:

.. code-block:: console

    $ pip install django-object-log

If you want to have the latest version, you can clone git repository:

.. code-block:: console

    $ git clone git://git.osuosl.org/gitolite/django/django_object_log

Then you'd have to manually install it:

.. code-block:: console

    $ cd django_object_log
    $ git checkout develop  # to get the latest development version
    $ python setup.py install


Configuration
=============

1. Add ``object_log`` to your project's ``INSTALLED_APPS`` setting.
2. Synchronize your database: ``./manage.py sync``
3. Add ``object_log.urls`` to ``urls.py`` if you wish to add generic views for
   displaying logs.
