"""
"""
from behave import *

import behave_restful._lang_imp.request_invoker as _invoker

@when('the request sends {method}')
def step_impl(context, method):
    invoker_function_name = 'send_' + method.lower()
    request_method = getattr(_invoker, invoker_function_name)
    request_method(context)