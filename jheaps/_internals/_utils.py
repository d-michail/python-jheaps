import sys
import ctypes

_c_inc_ref = ctypes.pythonapi.Py_IncRef
_c_inc_ref.argtypes = [ctypes.py_object]
_c_dec_ref = ctypes.pythonapi.Py_DecRef
_c_dec_ref.argtypes = [ctypes.py_object]


def _inc_ref(obj):
    """Increase the reference count of an object by one."""
    _c_inc_ref(obj)


def _dec_ref(obj):
    """Decrease the reference count of an object by one."""
    _c_dec_ref(obj)


def _ref_count(obj, normalize=True):
    """Get the reference count of an object
    """
    count = sys.getrefcount(obj)
    if normalize:
        # remove function argument, getrefcount temporary reference and function stack
        return count - 3
