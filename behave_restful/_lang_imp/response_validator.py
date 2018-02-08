"""
"""
import json

from assertpy import assert_that
import jsonschema

from behave_restful.xpy import HTTPStatus

def response_status_is(response, expected_status):
    """
    """
    expected_status = _as_numeric_status(expected_status)
    actual_status = response.status_code
    assert_that(actual_status).is_equal_to(expected_status)


def response_json_matches(response, schema_str):
    """
    """
    schema = json.loads(schema_str)
    json_body = response.json()
    jsonschema.validate(json_body, schema)
    


def _as_numeric_status(status):
    status = status.replace(' ', '_')
    numeric_status = getattr(HTTPStatus, status.upper(), None)
    if not numeric_status:
        numeric_status = int(status)
    return numeric_status

