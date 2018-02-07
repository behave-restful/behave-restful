import json

from assertpy import assert_that
from behave import *


@then('the context request url is equal to {expected_url}')
def step_impl(context, expected_url):
    assert_that(context.request_url).is_equal_to(expected_url)


@then('the context request json payload is equal to')
def step_impl(context):
    expected_payload = json.loads(context.text)
    assert_that(context.request_json_payload).is_equal_to(expected_payload)