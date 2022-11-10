"""
"""
import json

from assertpy import assert_that, fail
from jsonpath import jsonpath
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
    _validate_with_schema(json_body, schema)


def response_json_matches_defined_schema(context, schema_id):
    """
    """
    schema_id = context.vars.resolve(schema_id)
    schema = context.schemas.get(schema_id)
    json_body = context.response.json()
    _validate_with_schema(json_body, schema)


def response_json_at_path_is_equal_to(response, json_path, value):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).is_equal_to(eval(value)) for actual_value in values]
    

def response_json_at_path_is_not_equal_to(response, json_path, value):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).is_not_equal_to(eval(value)) for actual_value in values]


def response_json_at_path_starts_with(response, json_path, value):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).starts_with(eval(value)) for actual_value in values]


def response_json_at_path_ends_with(response, json_path, value):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).ends_with(eval(value)) for actual_value in values]


def response_json_at_path_contains(response, json_path, value):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).contains(eval(value)) for actual_value in values]


def response_json_at_path_does_not_contain(response, json_path, value):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).does_not_contain(eval(value)) for actual_value in values]
    

def response_json_at_path_is_null(response, json_path):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).is_none() for actual_value in values]


def response_json_at_path_is_not_null(response, json_path):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).is_not_none() for actual_value in values]


def response_json_at_path_is_true(response, json_path):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).is_true() for actual_value in values]


def response_json_at_path_is_false(response, json_path):
    """
    """
    values = _get_values(response.json(), json_path)
    [assert_that(actual_value).is_false() for actual_value in values]


def response_header_is_equal_to(response, header_name, value):
    """
    """
    actual_value = _get_header_values(response.headers, header_name)
    assert_that(actual_value).is_equal_to(value)


def _as_numeric_status(status):
    status = status.replace(' ', '_')
    numeric_status = getattr(HTTPStatus, status.upper(), None)
    if not numeric_status:
        numeric_status = int(status)
    return numeric_status


def _get_values(json_body, json_path):
    results = jsonpath(json_body, json_path)
    if not results: fail('Match not found at <{path}> for <{body}>'.format(path=json_path, body=json_body))
    return results

def _get_header_values(headers, header_name):
    result = headers.get(header_name)
    if not result: fail('Match not found at <{headers}> for <{header_name}>'.format(headers=headers, header_name=header_name))
    return result

def _validate_with_schema(json_body, schema)  :
    jsonschema.validate(json_body, schema)

