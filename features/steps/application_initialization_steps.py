import os

from assertpy import assert_that
from behave import *

@then('the context exposes the working directory')
def step_impl(context):
    assert_that(context.working_dir).is_equal_to(os.getcwd())


@then('the context exposes the test directory')
def step_impl(context):
    this_directory = os.path.dirname(__file__)
    expected_directory = os.path.abspath(os.path.join(this_directory, '..'))
    assert_that(context.test_dir).is_equal_to(expected_directory)