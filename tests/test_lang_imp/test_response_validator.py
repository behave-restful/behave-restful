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
                    "edition": 4,
                    "discounted": True
                },
                {
                    "category": "thriller",
                    "author": "Lee Child",
                    "title": "Never Go Back",
                    "isbn": None,
                    "price": 14.99,
                    "discounted": False
                },
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


    # response_json_at_path_is_equal_to()
    def test_matches_specified_property(self):
        path = '$.store.book[0].author'
        value = '"Nigel Rees"'
        self.given_json(self.json_body).should_be_equal(path, value)


    def test_matches_specified_double_property(self):
        path = '$.store.book[1].price'
        value = '12.99'
        self.given_json(self.json_body).should_be_equal(path, value)


    def test_matches_specified_integer_property(self):
        path = '$.store.book[3].edition'
        value = '4'
        self.given_json(self.json_body).should_be_equal(path, value)


    def test_evaluates_all_matches_found(self):
        path = '$.store.book[1:4].category'
        value = '"fiction"'
        self.given_json(self.json_body).should_be_equal(path, value)


    def test_evaluates_all_matches_and_fails_if_any_does_not_match(self):
        with self.assertRaises(AssertionError):
            path = '$.store.book[*].category'
            value = '"reference"'
            self.given_json(self.json_body).should_be_equal(path, value)


    def test_raises_if_specified_path_does_not_find_matches(self):
        with self.assertRaises(AssertionError):
            path = '$.not.a.path'
            value = 'no match'
            self.given_json(self.json_body).should_be_equal(path, value)


    # response_json_at_path_is_not_equal_to()
    def test_passes_if_string_property_does_not_match_value(self):
        path = '$.store.book[0].author'
        value = '"Tolkien"'
        self.given_json(self.json_body).should_not_be_equal(path, value)


    def test_passes_if_all_the_values_are_not_equal_to_specified_value(self):
        path = '$.store.book[1:4].category'
        value = '"reference"'
        self.given_json(self.json_body).should_not_be_equal(path, value)
    

    def test_raises_if_one_of_the_values_matches_specified_value(self):
        with self.assertRaises(AssertionError):
            path = '$.store.book[*].category'
            value = '"reference"'
            self.given_json(self.json_body).should_not_be_equal(path, value)

    # Additional comparison functions for straight values
    def test_passes_if_starts_with_value(self):
        path = '$.store.book[0].title'
        value = '"Sayings"'
        self.given_json(self.json_body).should_start_with(path, value)


    def test_raises_if_it_does_not_start_with_value(self):
        with self.assertRaises(AssertionError):
            path = '$.store.book[0].title'
            value = '"saying"'
            self.given_json(self.json_body).should_start_with(path, value)


    def test_passes_if_it_ends_with_value(self):
        path = '$.store.book[1].title'
        value = '"our"'
        self.given_json(self.json_body).should_end_with(path, value)


    def test_passes_if_contains_value(self):
        path = '$.store.book[3].title'
        value = '"of"'
        self.given_json(self.json_body).should_contain(path, value)


    def test_raises_if_does_not_contain_value(self):
        with self.assertRaises(AssertionError):
            path = '$.store.book[3].title'
            value = '"not"'
            self.given_json(self.json_body).should_contain(path, value)


    def test_passes_if_does_not_contain_value(self):
        path = '$.store.book[3].title'
        value = '"not"'
        self.given_json(self.json_body).should_not_contain(path, value)


    def test_raises_if_contains_value(self):
        with self.assertRaises(AssertionError):
            path = '$.store.book[3].title'
            value = '"of"'
            self.given_json(self.json_body).should_not_contain(path, value)


    def test_passes_if_value_is_null(self):
        path = '$.store.book[4].isbn'
        self.given_json(self.json_body).should_be_null(path)


    def test_raises_if_value_is_not_null(self):
        with self.assertRaises(AssertionError):
            path = '$.store.book[3].isbn'
            self.given_json(self.json_body).should_be_null(path)


    def test_passes_if_value_is_not_null(self):
        path = '$.store.book[3].isbn'
        self.given_json(self.json_body).should_not_be_null(path)


    def test_raises_if_value_is_null(self):
        with self.assertRaises(AssertionError):
            path = '$.store.book[4].isbn'
            self.given_json(self.json_body).should_not_be_null(path)


    def test_passes_if_value_is_true(self):
        path = '$.store.book[3].discounted'
        self.given_json(self.json_body).should_be_true(path)


    def test_raises_if_value_is_not_true(self):
        with self.assertRaises(AssertionError):
            path = '$.store.book[4].discounted'
            self.given_json(self.json_body).should_be_true(path)


    def test_passes_if_value_is_false(self):
        path = '$.store.book[4].discounted'
        self.given_json(self.json_body).should_be_false(path)


    def test_raises_if_value_is_not_false(self):
        with self.assertRaises(AssertionError):
            path = '$.store.book[3].discounted'
            self.given_json(self.json_body).should_be_false(path)



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


    def should_be_equal(self, json_path, expected_value):
        _validator.response_json_at_path_is_equal_to(self.response, json_path, expected_value)


    def should_not_be_equal(self, json_path, expected_value):
        _validator.response_json_at_path_is_not_equal_to(self.response, json_path, expected_value)
        

    def should_start_with(self, json_path, expected_value):
        _validator.response_json_at_path_starts_with(self.response, json_path, expected_value)


    def should_end_with(self, json_path, expected_value):
        _validator.response_json_at_path_ends_with(self.response, json_path, expected_value)

    
    def should_contain(self, json_path, expected_value):
        _validator.response_json_at_path_contains(self.response, json_path, expected_value)


    def should_not_contain(self, json_path, expected_value):
        _validator.response_json_at_path_does_not_contain(self.response, json_path, expected_value)


    def should_be_null(self, json_path):
        _validator.response_json_at_path_is_null(self.response, json_path)


    def should_not_be_null(self, json_path):
        _validator.response_json_at_path_is_not_null(self.response, json_path)


    def should_be_true(self, json_path):
        _validator.response_json_at_path_is_true(self.response, json_path)


    def should_be_false(self, json_path):
        _validator.response_json_at_path_is_false(self.response, json_path)


    

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