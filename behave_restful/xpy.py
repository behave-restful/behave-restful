"""
This module provides utilities to write cross-version python code.
"""
import sys

PYTHON_VERSION_INFO = sys.version_info
PYTHON_MAYOR_VERSION = PYTHON_VERSION_INFO[0]

if PYTHON_MAYOR_VERSION == 3:
    BASE_STRING_TYPE = str
else:
    BASE_STRING_TYPE = basestring



def is_string(value):
    """
    Returns whether the specified value is a version independent string.

    :param value:
        Value we want to evalute

    :return:
        Boolean indicating if the value is a string. In Python 2.7 is an 
        object derived from ``basestring`` and in Python 3.x is an instance
        of ``str``.
    """
    return isinstance(value, BASE_STRING_TYPE)


