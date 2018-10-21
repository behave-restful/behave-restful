"""
"""
from behave import *

import behave_restful._lang_imp.response_validator as _validate

@then('the response status is {status}')
def step_impl(context, status):
    _validate.response_status_is(context.response, status)


@then('the response json matches')
def step_impl(context):
    schema = context.vars.resolve(context.text)
    _validate.response_json_matches(context.response, schema)


@then('the response json matches defined schema {schema_id}')
def step_impl(context, schema_id):
    _validate.response_json_matches_defined_schema(context, schema_id)


@then('the response json at {json_path} is equal to {value_str}')
def step_impl(context, json_path, value_str):
    _invoke_match(_validate.response_json_at_path_is_equal_to, context, json_path, value_str)


@then('the response json at {json_path} is not equal to {value_str}')
def step_impl(context, json_path, value_str):
    _invoke_match(_validate.response_json_at_path_is_not_equal_to, context, json_path, value_str)


@then('the response json at {json_path} starts with {value_str}')
def step_impl(context, json_path, value_str):
    _invoke_match(_validate.response_json_at_path_starts_with, context, json_path, value_str)


@then('the response json at {json_path} ends with {value_str}')
def step_impl(context, json_path, value_str):
    _invoke_match(_validate.response_json_at_path_ends_with, context, json_path, value_str)


@then('the response json at {json_path} contains {value_str}')
def step_impl(context, json_path, value_str):
    _invoke_match(_validate.response_json_at_path_contains, context, json_path, value_str)


@then('the response json at {json_path} does not contain {value_str}')
def step_impl(context, json_path, value_str):
    _invoke_match(_validate.response_json_at_path_does_not_contain, context, json_path, value_str)


@then('the response json at {json_path} is null')
def step_impl(context, json_path):
    _check_value_with(_validate.response_json_at_path_is_null, context, json_path)


@then('the response json at {json_path} is not null')
def step_impl(context, json_path):
    _check_value_with(_validate.response_json_at_path_is_not_null, context, json_path)


@then('the response json at {json_path} is true')
def step_impl(context, json_path):
    _check_value_with(_validate.response_json_at_path_is_true, context, json_path)


@then('the response json at {json_path} is false')
def step_impl(context, json_path):
    _check_value_with(_validate.response_json_at_path_is_false, context, json_path)
    

def _invoke_match(func, context, json_path, value_str):
    json_path = context.vars.resolve(json_path)
    value_str = context.vars.resolve(value_str)
    func(context.response, json_path, value_str)


def _check_value_with(func, context, json_path):
    json_path = context.vars.resolve(json_path)
    func(context.response, json_path)
