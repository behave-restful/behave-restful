import unittest

from assertpy import assert_that, fail

import behave_restful._definitions as _definitions
import behave_restful._lang_imp.request_builder as _builder


class TestBuilderInterface(unittest.TestCase):

    def setUp(self):
        super(TestBuilderInterface, self).setUp()
        self.vars = {
            'BASE_URL': 'http://server.com',
            'resource': 'resource',
            'OBJECT_ID': 5,
            'OBJECT_NAME': 'resolved name',
            'PARAM1': 'resolved_param1',
            'PARAM2': 'resolved_param2'
        }
        self.vars_manager = _definitions.VarsManager()
        self.vars_manager.add_vars(self.vars)
        self.context = ContextDouble()
        self.context.vars = self.vars_manager


    def test_should_set_url_in_context(self):
        url = 'http://a/url'
        _builder.set_url(self.context, url)
        assert_that(self.context.request_url).is_equal_to(url)


    def test_embedded_variables_in_url_are_resolved(self):
        _builder.set_url(self.context, '${BASE_URL}/a/${resource}')
        assert_that(self.context.request_url).is_equal_to('http://server.com/a/resource')


    def test_should_set_payload_in_context(self):
        payload = """
        {
            "id": 1,
            "name": "an object"
        }
        """
        expected_payload = {
            'id': 1,
            'name': 'an object'
        }
        _builder.set_json_payload(self.context, payload)
        assert_that(self.context.request_json_payload).is_equal_to(expected_payload)


    def test_embedded_variables_in_payload_are_resolved(self):
        payload = """
        {
            "id": ${OBJECT_ID},
            "name": "${OBJECT_NAME}"
        }
        """
        expected_payload = {
            'id': 5,
            'name': 'resolved name'
        }
        _builder.set_json_payload(self.context, payload)
        assert_that(self.context.request_json_payload).is_equal_to(expected_payload)


    def test_request_parameters_are_set_in_context(self):
        actual_params = TableDouble()
        expected_params = {'id': '4',
                            'name': 'foo_bar'}
        _builder.set_request_params(self.context, actual_params)
        assert_that(self.context.request_params).is_equal_to(expected_params)


    def test_request_parameter_values_are_resolved(self):
        actual_params = TableDouble(resolve_values=True)
        expected_params = {'id': '5',
                           'name': 'resolved name'}
        _builder.set_request_params(self.context, actual_params)
        assert_that(self.context.request_params).is_equal_to(expected_params)


    def test_request_parameter_names_are_resolved(self):
        actual_params = TableDouble(resolve_names=True)
        expected_params = {'resolved_param1': 'foo',
                           'resolved_param2': 'bar'}
        _builder.set_request_params(self.context, actual_params)
        assert_that(self.context.request_params).is_equal_to(expected_params)

        

class ContextDouble(object):
    pass




class TableDouble(object):

    def __init__(self, resolve_values=False, resolve_names=False):
        self.resolve_values = resolve_values
        self.resolve_names = resolve_names


    def __iter__(self):
        if self.resolve_values:
            yield {'param': 'id',
                   'value': '${OBJECT_ID}'}
            yield {'param': 'name',
                   'value': '${OBJECT_NAME}'}
        elif self.resolve_names:
            yield {'param': '${PARAM1}',
                   'value': 'foo'}
            yield {'param': '${PARAM2}',
                   'value': 'bar'}
        else:
            yield {'param': 'id',
                   'value': '4'}
            yield {'param': 'name',
                   'value': 'foo_bar'}



if __name__=="__main__":
    unittest.main()