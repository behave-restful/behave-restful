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