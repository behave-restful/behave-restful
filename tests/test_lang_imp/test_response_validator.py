import json
import unittest

from assertpy import assert_that
import jsonschema.exceptions as jse

from behave_restful.xpy import HTTPStatus
import behave_restful._definitions as _definitions

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
        self.json_body = {
            "store": {
                "book": [ 
                { 
                    "category": "reference",
                    "author": "Nigel Rees",
                    "title": "Sayings of the Century",
                    "price": 8.95,
                    "edition": 1
                },
                { 
                    "category": "fiction",
                    "author": "Evelyn Waugh",
                    "title": "Sword of Honour",
                    "price": 12.99,
                    "edition": 2
                },
                { 
                    "category": "fiction",
                    "author": "Herman Melville",
                    "title": "Moby Dick",
                    "isbn": "0-553-21311-3",
                    "price": 8.99,
                    "edition": 3
                },
                { 
                    "category": "fiction",
                    "author": "J. R. R. Tolkien",
                    "title": "The Lord of the Rings",
                    "isbn": "0-395-19395-8",
                    "price": 22.99,
                    "edition": 4
                }
                ],
                "bicycle": {
                "color": "red",
                "price": 19.95
                }
            }
        }
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
        with self.assertRaises(ValueError):
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


    # response_json_matches_defined_schema()
    def test_matches_response_against_specified_schema(self):
        self.setup_context()
        self.given_json({
            'id': 1,
            'name': 'object name'
        }).validate_with('TEST_SCHEMA')


    def test_resolves_the_id_if_passed_as_variable(self):
        self.setup_context()
        self.setup_context()
        self.given_json({
            'id': 1,
            'name': 'object name'
        }).validate_with('${SCHEMA_ID}')


    # response_json_matches_at()
    def test_matches_specified_property(self):
        self.given_json(self.json_body).match('$.store.book[0].author', '"Nigel Rees"')


    def test_matches_specified_double_property(self):
        self.given_json(self.json_body).match('$.store.book[1].price', '12.99')


    def test_matches_specified_integer_property(self):
        self.given_json(self.json_body).match('$.store.book[3].edition', '4')


    def test_evaluates_all_matches_found(self):
        self.given_json(self.json_body).match('$.store.book[1:4].category', '"fiction"')


    def test_evaluates_all_matches_and_fails_if_any_does_not_match(self):
        with self.assertRaises(AssertionError):
            self.given_json(self.json_body).match('$.store.book[*].category', '"reference"')


    def test_raises_if_specified_path_does_not_find_matches(self):
        with self.assertRaises(AssertionError):
            self.given_json(self.json_body).match('$.not.a.path', 'no match')    


    def given_json(self, json_object):
        self.response.json_payload = json_object
        return self


    def setup_context(self):
        self.context = ContextDouble()
        self.context.response = self.response
        self.context.schemas = {
            'TEST_SCHEMA': json.loads(self.schema)
        }
        self.context.vars = _definitions.VarsManager()
        self.context.vars.add('SCHEMA_ID', 'TEST_SCHEMA')


    def validate(self):
        _validator.response_json_matches(self.response, self.schema)


    def validate_with(self, schema_id):
        _validator.response_json_matches_defined_schema(self.context, schema_id)


    def match(self, json_path, expected_value):
        _validator.response_json_matches_at(self.response, json_path, expected_value)
        


    

class ResponseDouble(object):
    def __init__(self):
        self.status_code = HTTPStatus.OK
        self.json_payload = None


    def json(self):
        if self.json_payload: return self.json_payload
        raise ValueError('No JSON object could be decoded')



class ContextDouble(object):
    def __init__(self):
        self.schemas = None
        self.response = None
        



if __name__=="__main__":
    unittest.main()