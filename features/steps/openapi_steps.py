from behave import *

import behave_restful.tools as brt

@given('an openapi file {filename}')
def step_impl(context, filename):
    filename = context.vars.resolve(filename)
    brt.add_openapi_schemas(filename, context)