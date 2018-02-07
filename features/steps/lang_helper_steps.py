import json

from assertpy import assert_that
from behave import *


@given('a test session')
def step_impl(context):
    context.session = SessionDouble()


@then('the context request url is equal to {expected_url}')
def step_impl(context, expected_url):
    assert_that(context.request_url).is_equal_to(expected_url)


@then('the context request json payload is equal to')
def step_impl(context):
    expected_payload = json.loads(context.text)
    assert_that(context.request_json_payload).is_equal_to(expected_payload)


@then('the session {name} property is {value}')
def step_impl(context, name, value):
    expected_value = eval(value)
    actual_value = getattr(context.session, name)
    assert_that(actual_value).is_equal_to(expected_value)




class SessionDouble(object):
    def __init__(self):
        self.response = None
        self.get_invoked = False
        self.post_invoked = False
        self.put_invoked = False
        self.delete_invoked = False
        self.request_url = None
        self.request_params = None
        self.request_data = None
        self.request_json = None
        self.request_kwargs = None


    def get(self, url, params=None, **kwargs):
        self.get_invoked = True
        self.request_url = url
        self.request_params = params
        self.request_kwargs = kwargs
        return self.response


    def post(self, url, data=None, json=None, **kwargs):
        self.post_invoked = True
        self.request_url = url
        self.request_data = data
        self.request_json = json
        self.request_kwargs = kwargs
        return self.response


    def put(self, url, data=None, **kwargs):
        self.put_invoked = True
        self.request_url = url
        self.request_data = data
        self.request_kwargs = kwargs
        return self.response


    def delete(self, url, **kwargs):
        self.delete_invoked = True
        self.request_url = url
        self.request_kwargs = kwargs
        return self.response