"""
"""
from assertpy import assert_that

from behave_restful.xpy import HTTPStatus

def response_status_is(response, expected_status):
    """
    """
    expected_status = _as_numeric_status(expected_status)
    actual_status = response.status_code
    assert_that(actual_status).is_equal_to(expected_status)


def _as_numeric_status(status):
    status = status.replace(' ', '_')
    numeric_status = getattr(HTTPStatus, status.upper(), None)
    if not numeric_status:
        numeric_status = int(status)
    return numeric_status
