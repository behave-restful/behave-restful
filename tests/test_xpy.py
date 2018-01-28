import unittest

from assertpy import assert_that

import behave_restful.xpy as xpy

class TestIsString(unittest.TestCase):

    def test_returns_true_if_string(self):
        assert_that(xpy.is_string('this is a string')).is_true()


    def test_returns_false_if_not_a_string(self):
        assert_that(xpy.is_string(1)).is_false()


if __name__=="__main__":
    unittest.main()