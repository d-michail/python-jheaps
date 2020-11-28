#ifndef __BACKEND_H
#define __BACKEND_H

#include <graal_isolate.h>
#include <jheaps_capi_types.h>

#if defined(__cplusplus)
extern "C" {
#endif

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

int jheaps_AHeap_D_insert_key(void *, double, void**);

int jheaps_AHeap_L_insert_key(void *, long long int, void**);

int jheaps_AHeap_D_insert_key_value(void *, double, long long int, void**);

int jheaps_AHeap_L_insert_key_value(void *, long long int, long long int, void**);

int jheaps_AHeap_find_min(void *, void**);

int jheaps_AHeap_delete_min(void *, void**);

int jheaps_AHeap_size(void *, long long*);

int jheaps_AHeap_isempty(void *, int*);

int jheaps_AHeap_clear(void *);

int jheaps_AHeapHandle_D_get_key(void *, double*);

int jheaps_AHeapHandle_L_get_key(void *, long long*);

int jheaps_AHeapHandle_get_value(void *, long long*);

int jheaps_AHeapHandle_set_value(void *, long long int);

int jheaps_AHeapHandle_D_decrease_key(void *, double);

int jheaps_AHeapHandle_L_decrease_key(void *, long long int);

int jheaps_AHeapHandle_delete(void *);

int jheaps_handles_destroy(void *);

int jheaps_handles_get_ccharpointer(void *, char**);

int jheaps_heap_create(heap_type_t, void**);

int jheaps_MAHeap_D_meld(void *, void *);

int jheaps_MAHeap_L_meld(void *, void *);



#if defined(__cplusplus)
}
#endif
#endif
