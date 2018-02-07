import unittest

from behave_restful.xpy import HTTPStatus

import behave_restful._lang_imp.response_validator as _validator




class TestResponseValidatorInterface(unittest.TestCase):

    def setUp(self):
        super(TestResponseValidatorInterface, self).setUp()
        self.response = ResponseDouble()


    def test_validates_status_code_if_specified_as_string_with_numeric_value(self):
        _validator.response_status_is(self.response, '200')


    def test_validates_status_code_if_specified_as_string_with_error_constant(self):
        _validator.response_status_is(self.response, 'OK')


    def test_validates_any_capitalization_of_status_code(self):
        _validator.response_status_is(self.response, 'Ok')


    def test_validates_status_if_specified_with_spaces(self):
        self.response.status_code = HTTPStatus.NOT_ACCEPTABLE
        _validator.response_status_is(self.response, 'NOT ACCEPTABLE')



class ResponseDouble(object):
    def __init__(self):
        self.status_code = HTTPStatus.OK
        



if __name__=="__main__":
    unittest.main()