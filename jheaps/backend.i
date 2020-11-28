%module backend

%{
#define SWIG_FILE_WITH_INIT
#include "backend.h"
%}


%include <typemaps.i>

// custom typemap to append void** types to the result
%typemap(in,numinputs=0,noblock=1) void **OUTPUT ($*1_ltype temp) {
    $1 = &temp;
}

%typemap(argout,noblock=1) void **OUTPUT {
    %append_output(SWIG_NewPointerObj(*$1, $*1_descriptor, SWIG_POINTER_NOSHADOW | %newpointer_flags));
}

%typemap(in,numinputs=0,noblock=1) char **OUTPUT ($*1_ltype temp) {
    $1 = &temp;
}

%typemap(argout,noblock=1) char **OUTPUT {
    %append_output(SWIG_FromCharPtr(($*1_ltype)*$1));
}

// convert a long to a void function pointer
%typemap(in) void *LONG_TO_FPTR { 
    $1 = PyLong_AsVoidPtr($input);    
}

// convert bytearray to c-string
%typemap(in) char *BYTEARRAY {
    if ($input != Py_None) { 
        if (!PyByteArray_Check($input)) {
            SWIG_exception_fail(SWIG_TypeError, "in method '" "$symname" "', argument "
                       "$argnum"" of type '" "$type""'");
        }
        $1 = (char*) PyByteArray_AsString($input);
    } else { 
        $1 = (char*) 0;
    }
}

enum status_t { 
    STATUS_SUCCESS = 0,
    STATUS_ERROR,
    STATUS_ILLEGAL_ARGUMENT,
    STATUS_UNSUPPORTED_OPERATION,
    STATUS_INDEX_OUT_OF_BOUNDS,
    STATUS_NO_SUCH_ELEMENT,
    STATUS_NULL_POINTER,
    STATUS_CLASS_CAST,
    STATUS_IO_ERROR,
};

enum heap_type_t {
    HEAP_TYPE_PAIRING = 0,
    HEAP_TYPE_RANKPAIRING,
    HEAP_TYPE_FIBONACCI,
};

// library init

void jheaps_init();

void jheaps_cleanup();

int jheaps_is_initialized();

// error

void jheaps_error_clear_errno();

int jheaps_error_get_errno();

char *jheaps_error_get_errno_msg();

void jheaps_error_print_stack_trace();

// vm

void jheaps_vmLocatorSymbol();

// exception handling
// grab result from C and throw python exception

%{
int raise_exception_on_error(int result) { 
    if (result != STATUS_SUCCESS) {
        switch(result) {
        case STATUS_ILLEGAL_ARGUMENT:
            PyErr_SetString(PyExc_ValueError, jheaps_error_get_errno_msg());
            break;
        case STATUS_UNSUPPORTED_OPERATION:
            PyErr_SetString(PyExc_ValueError, jheaps_error_get_errno_msg());
            break;
        case STATUS_INDEX_OUT_OF_BOUNDS:
            PyErr_SetString(PyExc_IndexError, jheaps_error_get_errno_msg());
            break;
        case STATUS_NO_SUCH_ELEMENT:
            PyErr_SetString(PyExc_KeyError, jheaps_error_get_errno_msg());
            break;
        case STATUS_NULL_POINTER:
            PyErr_SetString(PyExc_ValueError, jheaps_error_get_errno_msg());
            break;
        case STATUS_CLASS_CAST:
            PyErr_SetString(PyExc_TypeError, jheaps_error_get_errno_msg());
            break;
        case STATUS_IO_ERROR:
            PyErr_SetString(PyExc_IOError, jheaps_error_get_errno_msg());
            break;
        case STATUS_ERROR:
        default:
            PyErr_SetString(PyExc_RuntimeError, jheaps_error_get_errno_msg());
            break;
        }
        jheaps_error_clear_errno();
        return 1;
    }
    return 0;
}
%}

%exception { 
    $action
    if (raise_exception_on_error(result)) { 
        SWIG_fail;
    }
}

// ignore the integer return code
// we already handled this using the exception 
%typemap(out) int  "$result = SWIG_Py_Void();";


// Put some init code in python
%pythonbegin %{
# The Python-JHeaps library

from enum import Enum

%}

// create custom enums
%pythoncode %{

class HeapType(Enum):
    PAIRING = _backend.HEAP_TYPE_PAIRING
    RANKPAIRING = _backend.HEAP_TYPE_RANKPAIRING
    FIBONACCI = _backend.HEAP_TYPE_FIBONACCI
%}


int jheaps_AHeap_D_insert_key(void *, double, void** OUTPUT);

int jheaps_AHeap_L_insert_key(void *, long long int, void** OUTPUT);

int jheaps_AHeap_D_insert_key_value(void *, double, long long int, void** OUTPUT);

int jheaps_AHeap_L_insert_key_value(void *, long long int, long long int, void** OUTPUT);

int jheaps_AHeap_find_min(void *, void** OUTPUT);

int jheaps_AHeap_delete_min(void *, void** OUTPUT);

int jheaps_AHeap_size(void *, long long* OUTPUT);

int jheaps_AHeap_isempty(void *, int* OUTPUT);

int jheaps_AHeap_clear(void *);

int jheaps_AHeapHandle_D_get_key(void *, double* OUTPUT);

int jheaps_AHeapHandle_L_get_key(void *, long long* OUTPUT);

int jheaps_AHeapHandle_get_value(void *, long long* OUTPUT);

int jheaps_AHeapHandle_set_value(void *, long long int);

int jheaps_AHeapHandle_D_decrease_key(void *, double);

int jheaps_AHeapHandle_L_decrease_key(void *, long long int);

int jheaps_AHeapHandle_delete(void *);

int jheaps_handles_destroy(void *);

int jheaps_handles_get_ccharpointer(void *, char** OUTPUT);

int jheaps_heap_create(heap_type_t, void** OUTPUT);

int jheaps_MAHeap_D_meld(void *, void *);

int jheaps_MAHeap_L_meld(void *, void *);

