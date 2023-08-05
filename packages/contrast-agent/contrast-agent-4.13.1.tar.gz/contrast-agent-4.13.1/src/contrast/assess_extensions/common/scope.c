/*
 * Copyright © 2021 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/logging.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/threadlocal_storage.h>

#define DECREMENT_SCOPE(SCOPE, NAME) \
    do {                             \
        if ((SCOPE)->NAME > 0)       \
            (SCOPE)->NAME--;         \
    } while (0)

/* Get the scope for the current thread (NULL on failure) */
static thread_scope_t *get_scope(void) {
    thread_storage_t *storage;
    return (storage = get_thread_storage()) == NULL ? NULL : storage->scope;
}

inline void enter_contrast_scope(void) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL)
        return;

    scope->contrast_scope++;
}

inline void exit_contrast_scope(void) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL)
        return;

    if (scope->contrast_scope > 0)
        scope->contrast_scope--;
}

inline void enter_propagation_scope(void) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL)
        return;

    scope->propagation_scope++;
}

inline void exit_propagation_scope(void) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL)
        return;

    if (scope->propagation_scope > 0)
        scope->propagation_scope--;
}

inline int should_propagate(void) {
    thread_scope_t *scope = get_scope();

    if (scope == NULL) {
        return 0;
    }

    return !(scope->contrast_scope || scope->propagation_scope || scope->trigger_scope);
}

inline int in_eval_scope(void) {
    thread_scope_t *scope = get_scope();

    if (scope == NULL) {
        return 0;
    }

    return scope->eval_scope;
}

PyObject *set_exact_scope(PyObject *self, PyObject *py_target_scope) {
    thread_scope_t *current_scope;
    thread_scope_t target_scope;

    if ((current_scope = get_scope()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get scope state for this thread");
        return NULL;
    }

    if (!PyArg_ParseTuple(
            py_target_scope,
            "iiii",
            &target_scope.contrast_scope,
            &target_scope.propagation_scope,
            &target_scope.trigger_scope,
            &target_scope.eval_scope)) {
        PyErr_Format(PyExc_RuntimeError, "Failed to parse storage args from tuple");
        return NULL;
    }

    current_scope->contrast_scope = target_scope.contrast_scope;
    current_scope->propagation_scope = target_scope.propagation_scope;
    current_scope->trigger_scope = target_scope.trigger_scope;
    current_scope->eval_scope = target_scope.eval_scope;

    Py_RETURN_NONE;
}

PyObject *enter_scope(PyObject *self, PyObject *args) {
    ScopeLevel_t scope_id;
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get scope state for this thread");
        return NULL;
    }

    if (!PyArg_ParseTuple(args, "i", &scope_id)) {
        return NULL;
    }

    switch (scope_id) {
        case CONTRAST_SCOPE:
            scope->contrast_scope++;
            break;
        case PROPAGATION_SCOPE:
            scope->propagation_scope++;
            break;
        case TRIGGER_SCOPE:
            scope->trigger_scope++;
            break;
        case EVAL_SCOPE:
            scope->eval_scope++;
            break;
    }

    Py_RETURN_NONE;
}

PyObject *exit_scope(PyObject *self, PyObject *args) {
    ScopeLevel_t scope_id;
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get scope state for this thread");
        return NULL;
    }

    if (!PyArg_ParseTuple(args, "i", &scope_id))
        return NULL;

    switch (scope_id) {
        case CONTRAST_SCOPE:
            DECREMENT_SCOPE(scope, contrast_scope);
            break;
        case PROPAGATION_SCOPE:
            DECREMENT_SCOPE(scope, propagation_scope);
            break;
        case TRIGGER_SCOPE:
            DECREMENT_SCOPE(scope, trigger_scope);
            break;
        case EVAL_SCOPE:
            DECREMENT_SCOPE(scope, eval_scope);
            break;
    }

    Py_RETURN_NONE;
}

PyObject *in_scope(PyObject *self, PyObject *args) {
    ScopeLevel_t scope_id;
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get scope state for this thread");
        return NULL;
    }

    if (!PyArg_ParseTuple(args, "i", &scope_id))
        return NULL;

    switch (scope_id) {
        case CONTRAST_SCOPE:
            return PyBool_FromLong(scope->contrast_scope);
        case PROPAGATION_SCOPE:
            return PyBool_FromLong(scope->propagation_scope);
        case TRIGGER_SCOPE:
            return PyBool_FromLong(scope->trigger_scope);
        case EVAL_SCOPE:
            return PyBool_FromLong(scope->eval_scope);
    }

    Py_RETURN_FALSE;
}

PyObject *in_contrast_or_propagation_scope(PyObject *self, PyObject *ignored) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get scope state for this thread");
        return NULL;
    }

    return PyBool_FromLong(scope->contrast_scope | scope->propagation_scope);
}

int init_thread_scope(thread_scope_t **scope, const thread_scope_t *scope_level) {
    log_debug("init thread scope");

    if ((*scope = malloc(sizeof(**scope))) == NULL) {
        log_error("Failed to allocate scope for thread");
        return 0;
    }

    memcpy(*scope, scope_level, sizeof(**scope));

    return 1;
}

PyObject *get_thread_scope(PyObject *self, PyObject *ignored) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get scope state for this thread");
        return NULL;
    }

    return Py_BuildValue(
        "(iiii)",
        scope->contrast_scope,
        scope->propagation_scope,
        scope->trigger_scope,
        scope->eval_scope);
}

void destroy_scope(thread_scope_t *scope) {
    log_debug("destroy thread scope");

    if (scope != NULL) {
        free(scope);
    }
}
