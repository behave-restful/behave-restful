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
    json_path = context.vars.resolve(json_path)
    value_str = context.vars.resolve(value_str)
    _validate.response_json_matches_at(context.response, json_path, value_str)
