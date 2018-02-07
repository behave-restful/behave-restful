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
            'OBJECT_NAME': 'resolved name'
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

        

class ContextDouble(object):
    pass



if __name__=="__main__":
    unittest.main()