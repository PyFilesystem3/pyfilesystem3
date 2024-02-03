.. _implementers:

Implementing Filesystems
========================

With a little care, you can implement a PyFilesystem3 interface for any filesystem, which will allow it to work interchangeably with any of the built-in FS classes and tools.

To create a PyFilesystem3 interface, derive a class from :class:`~fs3.base.FS` and implement the :ref:`essential-methods`. This should give you a working FS class.

Take care to copy the method signatures *exactly*, including default values. It is also essential that you follow the same logic with regards to exceptions, and only raise exceptions in :mod:`~fs3.errors`.

Constructor
-----------

There are no particular requirements regarding how a PyFilesystem3 class is constructed, but be sure to call the base class ``__init__`` method with no parameters.


Thread Safety
-------------

All Filesystems should be *thread-safe*. The simplest way to achieve that is by using the ``_lock`` attribute supplied by the :class:`~fs3.base.FS` constructor. This is a ``RLock`` object from the standard library, which you can use as a context manager, so methods you implement will start something like this::

    with self._lock:
        do_something()

You aren't *required* to use ``_lock``. Just as long as calling methods on the FS object from multiple threads doesn't break anything.

Python Versions
---------------

PyFilesystem3 supports non-EoLed CPython 3.x and PyPy 3.x versions. At this time, that is CPython 3.8, 3.9, 3.10, 3.11, and 3.12 and PyPy 3.9 and 3.10.

You aren't obligated to support the same versions of Python that PyFilesystem3 itself supports, but it is recommended if your project is for general use.


Testing Filesystems
-------------------

To test your implementation, you can borrow the test suite used to test the built in filesystems. If your code passes these tests, then you can be confident your implementation will work seamlessly.

Here's the simplest possible example to test a filesystem class called ``MyFS``::

    import unittest
    from fs3.test import FSTestCases

    class TestMyFS(FSTestCases, unittest.TestCase):

        def make_fs(self):
            # Return an instance of your FS object here
            return MyFS()


You may also want to override some of the methods in the test suite for more targeted testing:

.. autoclass:: fs3.test.FSTestCases
    :members:

.. note::

    As of version 2.4.11 this project uses `pytest <https://pytest.org/en/latest/>`_ to run its tests.
    While it's completely compatible with ``unittest``-style tests, it's much more powerful and
    feature-rich. We suggest you take advantage of it and its plugins in new tests you write, rather
    than sticking to strict ``unittest`` features. For benefits and limitations, see `here <https://pytest.org/en/latest/unittest.html>`_.


.. _essential-methods:

Essential Methods
-----------------

The following methods MUST be implemented in a PyFilesystem3 interface.

* :meth:`~fs3.base.FS.getinfo` Get info regarding a file or directory.
* :meth:`~fs3.base.FS.listdir` Get a list of resources in a directory.
* :meth:`~fs3.base.FS.makedir` Make a directory.
* :meth:`~fs3.base.FS.openbin` Open a binary file.
* :meth:`~fs3.base.FS.remove` Remove a file.
* :meth:`~fs3.base.FS.removedir` Remove a directory.
* :meth:`~fs3.base.FS.setinfo` Set resource information.

.. _non-essential-methods:

Non - Essential Methods
-----------------------

The following methods MAY be implemented in a PyFilesystem3 interface.

These methods have a default implementation in the base class, but may be overridden if you can supply a more optimal version.

Exactly which methods you should implement depends on how and where the data is stored. For network filesystems, a good candidate to implement, is the ``scandir`` method which would otherwise call a combination of ``listdir`` and ``getinfo`` for each file.

In the general case, it is a good idea to look at how these methods are implemented in :class:`~fs3.base.FS`, and only write a custom version if it would be more efficient than the default.

* :meth:`~fs3.base.FS.appendbytes`
* :meth:`~fs3.base.FS.appendtext`
* :meth:`~fs3.base.FS.close`
* :meth:`~fs3.base.FS.copy`
* :meth:`~fs3.base.FS.copydir`
* :meth:`~fs3.base.FS.create`
* :meth:`~fs3.base.FS.desc`
* :meth:`~fs3.base.FS.download`
* :meth:`~fs3.base.FS.exists`
* :meth:`~fs3.base.FS.filterdir`
* :meth:`~fs3.base.FS.getmeta`
* :meth:`~fs3.base.FS.getospath`
* :meth:`~fs3.base.FS.getsize`
* :meth:`~fs3.base.FS.getsyspath`
* :meth:`~fs3.base.FS.gettype`
* :meth:`~fs3.base.FS.geturl`
* :meth:`~fs3.base.FS.hassyspath`
* :meth:`~fs3.base.FS.hasurl`
* :meth:`~fs3.base.FS.isclosed`
* :meth:`~fs3.base.FS.isempty`
* :meth:`~fs3.base.FS.isdir`
* :meth:`~fs3.base.FS.isfile`
* :meth:`~fs3.base.FS.islink`
* :meth:`~fs3.base.FS.lock`
* :meth:`~fs3.base.FS.makedirs`
* :meth:`~fs3.base.FS.move`
* :meth:`~fs3.base.FS.movedir`
* :meth:`~fs3.base.FS.open`
* :meth:`~fs3.base.FS.opendir`
* :meth:`~fs3.base.FS.readbytes`
* :meth:`~fs3.base.FS.readtext`
* :meth:`~fs3.base.FS.removetree`
* :meth:`~fs3.base.FS.scandir`
* :meth:`~fs3.base.FS.settimes`
* :meth:`~fs3.base.FS.touch`
* :meth:`~fs3.base.FS.upload`
* :meth:`~fs3.base.FS.validatepath`
* :meth:`~fs3.base.FS.writebytes`
* :meth:`~fs3.base.FS.writefile`
* :meth:`~fs3.base.FS.writetext`

.. _helper-methods:

Helper Methods
--------------

These methods SHOULD NOT be implemented.

Implementing these is highly unlikely to be worthwhile.

* :meth:`~fs3.base.FS.check`
* :meth:`~fs3.base.FS.getbasic`
* :meth:`~fs3.base.FS.getdetails`
* :meth:`~fs3.base.FS.hash`
* :meth:`~fs3.base.FS.match`
* :meth:`~fs3.base.FS.tree`
