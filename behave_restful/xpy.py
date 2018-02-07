"""
This module provides utilities to write cross-version python code.
"""
import sys

py_version = sys.version_info

if py_version.major == 3:
    BASE_STRING_TYPE = str
    
else:
    BASE_STRING_TYPE = basestring
    

if py_version.major == 3 and py_version.minor >= 5:
    from http import HTTPStatus as HTTPStatus
elif py_version.major == 3 and py_version.minor < 5:
    import http.client as HTTPStatus
else:
    import httplib as HTTPStatus



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


