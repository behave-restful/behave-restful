import json.decoder as jd
import unittest

from assertpy import assert_that
import jsonschema.exceptions as jse

from behave_restful.xpy import HTTPStatus

import behave_restful._lang_imp.response_validator as _validator




class TestResponseValidatorInterface(unittest.TestCase):

    def setUp(self):
        super(TestResponseValidatorInterface, self).setUp()
        self.schema = """
        {
            "title": "SampleJson",
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "name": {"type": "string"}
            },
            "required": ["id", "name"]
        }
        """
        self.response = ResponseDouble()        


    # response_status_is()
    def test_validates_status_code_if_specified_as_string_with_numeric_value(self):
        _validator.response_status_is(self.response, '200')


    def test_validates_status_code_if_specified_as_string_with_error_constant(self):
        _validator.response_status_is(self.response, 'OK')


    def test_validates_any_capitalization_of_status_code(self):
        _validator.response_status_is(self.response, 'Ok')


    def test_validates_status_if_specified_with_spaces(self):
        self.response.status_code = HTTPStatus.NOT_ACCEPTABLE
        _validator.response_status_is(self.response, 'NOT ACCEPTABLE')


    # response_json_matches()
    def test_validates_json_against_specified_schema(self):
        self.given_json({
            'id': 1,
            'name': 'object name'
        }).validate()


    def test_raises_if_schema_is_not_valid_json(self):
        self.schema = """
        {
            "not": "valid:
            "missing": "comma"
        }
        """
        with self.assertRaises(jd.JSONDecodeError):
            self.given_json({
                'id': 1,
                'name': 'object name'
            }).validate()


    def test_raises_if_response_does_not_contain_valid_json(self):
        with self.assertRaises(ValueError):
            self.validate()


    def test_raises_if_payload_does_not_validate(self):
        with self.assertRaises(jse.ValidationError):
            self.given_json({
                'id': 1
            }).validate()


    def test_raises_if_schema_is_invalid(self):
        with self.assertRaises(jse.SchemaError):
            self.schema = """
            {
                "not": "valid schema",
                "but": "Valid json"
            }
            """
            self.given_json({
                'id': 1
            }).validate()


    def given_json(self, json_object):
        self.response.json_payload = json_object
        return self


    def validate(self):
        _validator.response_json_matches(self.response, self.schema)
        


    

class ResponseDouble(object):
    def __init__(self):
        self.status_code = HTTPStatus.OK
        self.json_payload = None


    def json(self):
        if self.json_payload: return self.json_payload
        raise ValueError('No JSON object could be decoded')
        



if __name__=="__main__":
    unittest.main()