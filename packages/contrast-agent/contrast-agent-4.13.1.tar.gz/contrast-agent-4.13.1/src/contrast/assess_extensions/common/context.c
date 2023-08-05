/*
 * Copyright © 2021 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/context.h>
#include <contrast/assess/threadlocal_storage.h>

/* Get the request context for the current thread (NULL on failure) */
static PyObject *get_context(void) {
    thread_storage_t *storage;
    return (storage = get_thread_storage()) == NULL ? NULL : storage->context;
}

PyObject *get_thread_context(PyObject *self, PyObject *ignored) {
    PyObject *context;

    if ((context = get_context()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get context for this thread");
        return NULL;
    }

    /* We're giving the caller a reference to context, so we must INCREF it.
       When this reference falls out of scope in Python, it's automatically
       DECREF-ed. Failing to INCREF here causes all sorts of strange issues. */
    Py_INCREF(context);
    return context;
}

PyObject *set_thread_context(PyObject *self, PyObject *new_context) {
    thread_storage_t *storage;
    PyObject *old_context;

    if ((storage = get_thread_storage()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get storage for this thread");
        return NULL;
    }

    /* We do this because Py_DECREF can cause arbitrary python code to execute,
       so we must increment new_context's refcount before decrementing the old
     */
    old_context = storage->context;
    init_context(&storage->context, new_context);
    destroy_context(old_context);

    Py_RETURN_NONE;
}

/* Set this thread's request context to initial_context. Passing NULL will cause
   us to set the request context to None. */
void init_context(PyObject **context, PyObject *new_context) {
    if (new_context == NULL) {
        new_context = Py_None;
    }
    Py_INCREF(new_context);
    *context = new_context;
}

void destroy_context(PyObject *context) {
    Py_XDECREF(context);
}
