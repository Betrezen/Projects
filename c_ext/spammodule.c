#include <Python.h>

static PyObject* SpamError;

static PyMethodDef SpamMethods[];

PyMODINIT_FUNC initspam(void)  // init module after import
{
	PyObject* m;

	m = Py_InitModule("spam", SpamMethods);
	if (m == NULL)
		return;

	SpamError = PyErr_NewException("spam.SpamError", NULL, NULL);
	Py_INCREF(SpamError);
	PyModule_AddObject(m, "SpamError", SpamError);
}

static PyObject* spam_system(PyObject* self, PyObject* args)
{
	const char* command;
	int status_code;

	if (!PyArg_ParseTuple(args, "s", &command))  // from python to c: "s" means string
		return NULL;  // Error case

	status_code = system(command);

	if (status_code < 0)
	{
        PyErr_SetString(SpamError, "System command failed");
        return NULL;
    }

	return Py_BuildValue("i", status_code);  // from c to python: "i" means int
}

static PyMethodDef SpamMethods[] = {
    {"system",  spam_system, METH_VARARGS, "Execute a shell command."},
    {NULL, NULL, 0, NULL}  /* Sentinel */
};
