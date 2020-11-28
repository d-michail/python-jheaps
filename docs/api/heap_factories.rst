
.. _heap_factories:

Heap Factories
**************

.. currentmodule:: jheaps

Creating heaps can be accomplished using factory methods.

AddressableHeaps
^^^^^^^^^^^^^^^^

The main factory function which creates addressable heaps is :py:meth:`jheaps.create_heap`. 
Depending on the given parameters different types of heaps can be represented. All heaps
returned by this function are instances of :py:class:`jheaps.types.AddressableHeap`.
Most users should create graphs using this function:

.. autofunction:: jheaps.create_heap


