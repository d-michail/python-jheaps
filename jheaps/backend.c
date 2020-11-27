#include <stdlib.h>
#include <stdio.h>

#include <jheaps_capi_types.h>
#include <jheaps_capi.h>

#ifdef _WIN32
#define THREAD_LOCAL __declspec( thread )
#else
#define THREAD_LOCAL __thread 
#endif

// single graalVM isolate
static graal_isolate_t *isolate = NULL;

// thread local variable
static THREAD_LOCAL graal_isolatethread_t *thread = NULL;

// library init
void jheaps_init() {
    // do we need to synchronize here, or does the GIL protect us?
    if (isolate == NULL) { 
        // create isolate and attach thread
        if (graal_create_isolate(NULL, &isolate, &thread) != 0) {
            fprintf(stderr, "graal_create_isolate error\n");
            exit(EXIT_FAILURE);
        }
    } else if (thread == NULL) {
        // attach thread
        if (graal_attach_thread(isolate, &thread) != 0) { 
            fprintf(stderr, "graal_attach_thread error\n");
            exit(EXIT_FAILURE);
        }
    }
}

// library cleanup
void jheaps_cleanup() {
    // let the JVM cleanup for itself
}

int jheaps_is_initialized() { 
    return thread != NULL && isolate != NULL;
}

#define LAZY_THREAD_ATTACH \
    if (thread == NULL) { \
        if (graal_attach_thread(isolate, &thread) != 0) {    \
            fprintf(stderr, "graal_attach_thread error\n");  \
            exit(EXIT_FAILURE);                              \
        }                                                    \
    }

// error

void jheaps_error_clear_errno() {
    LAZY_THREAD_ATTACH
    jheaps_capi_error_clear_errno(thread);
}

status_t jheaps_error_get_errno() { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_error_get_errno(thread);
}

char * jheaps_error_get_errno_msg() {
    LAZY_THREAD_ATTACH
    return jheaps_capi_error_get_errno_msg(thread);
}

void jheaps_error_print_stack_trace() { 
    LAZY_THREAD_ATTACH
    jheaps_capi_error_print_stack_trace(thread);
}

// vm

void jheaps_vmLocatorSymbol() {
    LAZY_THREAD_ATTACH
    vmLocatorSymbol(thread);
}

// attribute store

int jheaps_AHeap_D_insert_key(void *heap, double key, void** res) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeap_D_insert_key(thread, heap, key, res);
}

int jheaps_AHeap_D_insert_key_value(void *heap, double key, long long int value, void** res) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeap_D_insert_key_value(thread, heap, key, value, res);
}

int jheaps_AHeap_find_min(void *heap, void** res) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeap_find_min(thread, heap, res);
}

int jheaps_AHeap_delete_min(void *heap, void** res) {
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeap_delete_min(thread, heap, res);
}

int jheaps_AHeap_size(void *heap, long long* res) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeap_size(thread, heap, res);
}

int jheaps_AHeap_isempty(void *heap, int* res) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeap_isempty(thread, heap, res);
}

int jheaps_AHeap_clear(void *heap) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeap_clear(thread, heap);
}

int jheaps_AHeapHandle_D_get_key(void *handle, double* res) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeapHandle_D_get_key(thread, handle, res);
}

int jheaps_AHeapHandle_get_value(void *handle, long long* res) {
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeapHandle_get_value(thread, handle, res);
}

int jheaps_AHeapHandle_set_value(void *handle, long long int value) {
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeapHandle_set_value(thread, handle, value);
}

int jheaps_AHeapHandle_D_decrease_key(void *handle, double key) {
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeapHandle_D_decrease_key(thread, handle, key);
}

int jheaps_AHeapHandle_delete(void *handle) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_AHeapHandle_delete(thread, handle);
}

int jheaps_handles_destroy(void *handle) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_handles_destroy(thread, handle);
}

int jheaps_handles_get_ccharpointer(void *handle, char** res) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_handles_get_ccharpointer(thread, handle, res);
}

int jheaps_heap_create(heap_type_t type, void** res) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_heap_create(thread, type, res);
}

int jheaps_MAHeap_D_meld(void *heap1, void *heap2) { 
    LAZY_THREAD_ATTACH
    return jheaps_capi_MAHeap_D_meld(thread, heap1, heap2);
}


