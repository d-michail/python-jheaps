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

from ._internals._heaps import (
    _create_heap,
    HeapType as _HeapType,
)

def create_dary(key_type=float, d=4, explicit=False):
    if explicit: 
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT
    else: 
        heap_type = _HeapType.HEAP_TYPE_ADDRESSABLE_DARY_IMPLICIT
    
    return _create_heap()
    pass


def create_binary(key_type=float, explicit=False, weak=False):
    pass


def create_fibonacci(key_type=float, simple=False, double_ended=False):
    if simple:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI_SIMPLE
    elif double_ended:
        heap_type = (
            _HeapType.HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_FIBONACCI_REFLECTED
        )
    else:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_FIBONACCI

    return _create_heap(key_type, heap_type)


def create_pairing(key_type=float, rank=False, costless_meld=False, double_ended=False):
    if rank:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_RANKPAIRING
    elif costless_meld:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_COSTLESSMELD_PAIRING
    elif double_ended:
        heap_type = (
            _HeapType.HEAP_TYPE_DOUBLEENDED_MERGEABLE_ADDRESSABLE_PAIRING_REFLECTED
        )
    else:
        heap_type = _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_PAIRING

    return _create_heap(key_type, heap_type)


def create_hollow(key_type=float):
    return _create_heap(key_type, _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_HOLLOW)


def create_leftist(key_type=float):
    return _create_heap(key_type, _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_LEFTIST)


def create_skew(key_type=float):
    return _create_heap(key_type, _HeapType.HEAP_TYPE_MERGEABLE_ADDRESSABLE_SKEW)    

