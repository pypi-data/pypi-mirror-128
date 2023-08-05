/*
 * Copyright © 2021 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_CONTEXT_H_
#define _ASSESS_CONTEXT_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/threadlocal_storage.h>

PyObject *get_thread_context(PyObject *, PyObject *);
PyObject *set_thread_context(PyObject *, PyObject *);

void init_context(PyObject **, PyObject *);
void destroy_context(PyObject *);

#endif /* _ASSESS_CONTEXT_H_ */
