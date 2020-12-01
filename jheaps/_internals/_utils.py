import sys
import ctypes

_c_inc_ref = ctypes.pythonapi.Py_IncRef
_c_inc_ref.argtypes = [ctypes.py_object]
_c_dec_ref = ctypes.pythonapi.Py_DecRef
_c_dec_ref.argtypes = [ctypes.py_object]


def _inc_ref(obj):
    """Increase the reference count of an object by one."""
    _c_inc_ref(obj)


def _inc_ref_by_id(id):
    """Increase the reference count of an object given by its id."""
    _c_inc_ref(_id_to_obj(id))


def _dec_ref(obj):
    """Decrease the reference count of an object by one."""
    _c_dec_ref(obj)


def _dec_ref_by_id(id):
    """Decrease the reference count of an object given by its id."""
    _c_inc_ref(_id_to_obj(id))


def _ref_count(obj, normalize=True):
    """Get the reference count of an object
    """
    count = sys.getrefcount(obj)
    if normalize:
        # remove function argument, getrefcount temporary reference and function stack
        return count - 3


def _id_to_obj(id):
    """Cast an id to an object. Note that this method if 
       called on non-existent object, will crash Python.
    """
    return ctypes.cast(id, ctypes.py_object).value


def _id_comparator(a_id, b_id): 
    """A comparator which accepts as input the ids of two python objects
    and compares them.
    """
    a = _id_to_obj(a_id)
    b = _id_to_obj(b_id)

    if a.__lt__(b): 
        return -1
    if a.__eq(b): 
        return 0
    return 1