"""
Python-JHeaps Library
~~~~~~~~~~~~~~~~~~~~~

JHeaps is a library providing state-of-the-art heap data structures.

See https://github.com/d-michail/python-jheaps for more details.
"""

from .__version__ import __title__, __description__, __url__
from .__version__ import __version__, __backend_version__
from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__

# Initialize with backend and setup module cleanup
from . import backend
import atexit

backend.jheaps_init()
del backend


def _module_cleanup_function():
    from . import backend

    backend.jheaps_cleanup()


atexit.register(_module_cleanup_function)
del atexit

# Set default logging handler to avoid "No handler found" warnings.
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

from . import (
    types,
)

from ._internals._factories import (
    _HeapType,
    _create_heap,
    _create_addressable_heap,
)


def create_addressable_dary_heap(key_type=float, value_type=int, d=4, explicit=False):
    if explicit:
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT
    else:
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT

    return _create_addressable_heap(heap_type, key_type, value_type)


def create_weak_binary_heap(key_type=float, bulk_insert=False):
    if bulk_insert:
        heap_type = _HeapType.HEAP_TYPE_BINARY_IMPLICIT_WEAK_BULKINSERT
    else:
        heap_type = _HeapType.HEAP_TYPE_BINARY_IMPLICIT_WEAK

    return _create_heap(key_type, heap_type)


def create_implicit_binary_heap(key_type=float):
    """Create a binary heap.

    :param key_type: the key type
    :type key_type: int or float
    """
    heap_type = _HeapType.HEAP_TYPE_BINARY_IMPLICIT
    return _create_heap(key_type, heap_type)


def create_addressable_binary_heap(key_type=float, value_type=int, explicit=False):
    """Create a binary heap.

    :param key_type: the key type
    :type key_type: int or float
    :param explicit: if true explicit, otherwise implicit (array-based)
    """
    if explicit:
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_BINARY_EXPLICIT
    else:
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_BINARY_IMPLICIT

    return _create_addressable_heap(heap_type, key_type, value_type)


def create_addressable_fibonacci_heap(
    key_type=float, value_type=int, simple=False, double_ended=False
):
    if simple:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI_SIMPLE
    elif double_ended:
        heap_type = (
            _HeapType.HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_FIBONACCI_REFLECTED
        )
    else:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI

    return _create_addressable_heap(heap_type, key_type, value_type)


def create_addressable_pairing_heap(
    key_type=float, value_type=int, rank=False, costless_meld=False, double_ended=False
):
    if rank:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING_RANK
    elif costless_meld:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING_COSTLESSMELD
    elif double_ended:
        heap_type = (
            _HeapType.HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_PAIRING_REFLECTED
        )
    else:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING

    return _create_addressable_heap(heap_type, key_type, value_type)


def create_addressable_hollow_heap(key_type=float, value_type=int):
    """Create an addressable hollow heap.

    :param key_type: the key type
    :type key_type: int, float or object
    """
    return _create_addressable_heap(
        _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_HOLLOW, key_type, value_type
    )


def create_addressable_leftist_heap(key_type=float, value_type=int):
    return _create_addressable_heap(
        _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_LEFTIST, key_type, value_type
    )


def create_addressable_skew_heap(key_type=float, value_type=int):
    return _create_addressable_heap(
        _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_SKEW, key_type, value_type
    )


def create_addressable_radix_heap(key_type=float, value_type=int):
    if key_type == float:
        heap_type = _HeapType.HEAP_TYPE_MONOTONE_ADDRESSABLE_DOUBLE_RADIX
    elif key_type == int:
        heap_type = _HeapType.HEAP_TYPE_MONOTONE_ADDRESSABLE_LONG_RADIX
    else:
        raise ValueError("Radix heaps support float or int keys")

    # TODO: fixme here (min, max)
    return _create_addressable_heap(heap_type, key_type, value_type)


def create_radix_heap(key_type=float):
    if key_type == float:
        heap_type = _HeapType.HEAP_TYPE_MONOTONE_DOUBLE_RADIX
    elif key_type == int:
        heap_type = _HeapType.HEAP_TYPE_MONOTONE_LONG_RADIX

    # TODO: fixme here (min, max)
    return _create_heap(key_type, heap_type)
