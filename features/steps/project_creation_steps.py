import filecmp
import os

from assertpy import assert_that, fail
from behave import *

import behave_restful.app as app

@given('br-init is run with {location}')
def step_impl(context, location):
    context.location_param = None if location == 'no parameters' else location
    project_folder = context.location_param or 'features'
    context.project_created_dir = os.path.join(os.getcwd(), project_folder)


@when('the application executes')
def step_impl(context):
    try:
        app.BrInitApp().init_project(context.location_param)
    except Exception as err:
        context.exception_raised = err


@then('the project is created at {folder} folder')
def step_impl(context, folder):
    result = filecmp.dircmp(context.project_src_dir, context.project_created_dir)
    assert_that(result.diff_files).is_empty()


@then('an exception is raised')
def step_impl(context):
    if not 'exception_raised' in context:
        fail('Exception not raised')
