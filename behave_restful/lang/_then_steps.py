"""
"""
from behave import *

import behave_restful._lang_imp.response_validator as _validate

@then('the response status is {status}')
def step_impl(context, status):
    _validate.response_status_is(context.response, status)