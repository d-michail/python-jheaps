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


def create_dary(key_type=float, use_int_values=True, d=4, explicit=False):
    if explicit: 
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT
    else: 
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT
    
    return _create_addressable_heap(heap_type, key_type, use_int_values)


def create_weak_binary(key_type=float, bulk_insert=False):
    if bulk_insert:
        heap_type = _HeapType.HEAP_TYPE_BINARY_IMPLICIT_WEAK_BULKINSERT
    else:
        heap_type = _HeapType.HEAP_TYPE_BINARY_IMPLICIT_WEAK
    
    return _create_heap(key_type, heap_type)


def create_binary(key_type=float, use_int_values=True, explicit=False, addressable=False):
    """Create a binary heap. 

    :param key_type: the key type
    :type key_type: int or float    
    :param explicit: if true explicit, otherwise implicit (array-based)
    :param addressable: if true addressable, otherwise not. Only valid for implicit
        since explicit are by default addressable
    """
    if explicit:
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_BINARY_EXPLICIT
        return _create_addressable_heap(heap_type, key_type, use_int_values)
    else: 
        if addressable: 
            heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_BINARY_IMPLICIT
            return _create_addressable_heap(heap_type, key_type, use_int_values)
        else:
            heap_type = _HeapType.HEAP_TYPE_BINARY_IMPLICIT
            return _create_heap(key_type, heap_type)


def create_fibonacci(key_type=float, use_int_values=True, simple=False, double_ended=False):
    if simple:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI_SIMPLE
    elif double_ended:
        heap_type = (
            _HeapType.HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_FIBONACCI_REFLECTED
        )
    else:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI

    return _create_addressable_heap(heap_type, key_type, use_int_values)


def create_pairing(key_type=float, use_int_values=True, rank=False, costless_meld=False, double_ended=False):
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

    return _create_addressable_heap(heap_type, key_type, use_int_values)


def create_hollow(key_type=float, use_int_values=True):
    """Create a hollow heap.

    :param key_type: the key type
    :type key_type: int or float
    """
    return _create_addressable_heap(_HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_HOLLOW, key_type, use_int_values)


def create_leftist(key_type=float, use_int_values=True):
    return _create_addressable_heap(_HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_LEFTIST, key_type, use_int_values)


def create_skew(key_type=float, use_int_values=True):
    return _create_addressable_heap(_HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_SKEW, key_type, use_int_values)    


def create_radix(key_type=float, use_int_values=True, addressable=False):
    if addressable: 
        if key_type == float: 
            heap_type = _HeapType.HEAP_TYPE_MONOTONE_ADDRESSABLE_DOUBLE_RADIX
        elif key_type == int:
            heap_type = _HeapType.HEAP_TYPE_MONOTONE_ADDRESSABLE_LONG_RADIX
    else:
        if key_type == float: 
            heap_type = _HeapType.HEAP_TYPE_MONOTONE_DOUBLE_RADIX
        elif key_type == int:
            heap_type = _HeapType.HEAP_TYPE_MONOTONE_LONG_RADIX

    if addressable:
        return _create_addressable_heap(heap_type, key_type, use_int_values)
    else:
        return _create_heap(key_type, heap_type)
