import os
import unittest

from assertpy import assert_that

import behave_restful._definitions as br_definitions


class TestDefinitionInitializer(unittest.TestCase):

    def setUp(self):
        # Mocks context expected properties
        self.context_mock = self
        self.config = self
        self.userdata = {}
        self.test_dir = 'test_dir'
        self.initializer = DefinitionInitializerSpy()
        

    def test_adds_definitions_directory_to_search_path(self):
        self.with_initializer()
        assert_that(self.initializer.added_search_path).is_equal_to(os.path.join(self.test_dir, 'definitions'))


    def test_loads_definition_if_specifed(self):
        self.userdata.update(definition='dev')
        self.with_initializer()
        assert_that(self.initializer.loaded_definition).is_equal_to('dev')


    def test_does_not_load_definition_if_not_specified(self):
        self.with_initializer()
        assert_that(self.initializer.loaded_definition).is_none()


    def test_raises_if_definition_module_cannot_be_imported(self):
        self.userdata.update(definition='dev')
        self.initializer.definition_module = None
        with self.assertRaises(br_definitions.DefinitionNotFoundError):
            self.with_initializer()


    def test_invokes_definition_module_initialization_with_context(self):
        self.userdata.update(definition='dev')
        self.with_initializer()
        assert_that(self.initializer.specified_context).is_same_as(self.context_mock)


    def test_invoked_context_has_a_vars_manager(self):
        self.userdata.update(definition='dev')
        self.with_initializer()
        assert_that(self.initializer.specified_context.vars).is_instance_of(br_definitions.VarsManager)


    def with_initializer(self):
        self.initializer.initialize(self.context_mock)



class DefinitionInitializerSpy(br_definitions.DefinitionInitializer):
    def __init__(self):
        self.added_search_path = None
        self.loaded_definition = None
        self.definition_module = self
        self.specified_context = None


    def _add_to_search_path(self, *path_tokens):
        self.added_search_path = os.path.join(*path_tokens)


    def _load_definition(self, definition_name):
        self.loaded_definition = definition_name
        return self.definition_module


    def initialize_definition(self, context):
        self.specified_context = context
        

class TestVarsManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.environment_var = 'TEST_ENVIRONMENT_VAR'
        cls.environment_var_value = 'environment_value'
        os.environ[cls.environment_var] = cls.environment_var_value

    def setUp(self):
        self.string_var = 'STRING_VAR'
        self.string_var_value = 'the string value'
        self.int_var = 'INT_VAR'
        self.int_var_value = 1
        self.composed_var = 'COMPOSED_VAR'
        self.composed_var_value =  '${STRING_VAR} and ${INT_VAR}'
        self.composed_var_no_resolution = 'COMPOSED_NO_RESOLUTION'
        self.composed_var_no_resolution_value = 'this has ${UNDEFINED}'
        self.defined_vars = {
            self.string_var: self.string_var_value,
            self.int_var: self.int_var_value,
            self.composed_var: self.composed_var_value,
            self.composed_var_no_resolution: self.composed_var_no_resolution_value,
        }
        self.manager = br_definitions.VarsManager()
        self.manager.add_vars(self.defined_vars)

    def test_returns_specified_variable_value(self):
        self.assert_var(self.string_var).is_equal_to(self.string_var_value)


    def test_returns_specified_value_as_specified_type(self):
        self.assert_var(self.int_var).is_equal_to(self.int_var_value)


    def test_returns_none_if_variable_not_defined(self):
        self.assert_var('UNDEFINED').is_none()


    def test_returns_specified_default_value_if_variable_not_defined(self):
        def_value = 'default'
        actual_value = self.manager.get('UNDEFINED', def_value)
        assert_that(actual_value).is_equal_to(def_value)


    def test_additional_variable_definitions_can_be_added(self):
        self.setup_additional_vars()
        self.manager.add_vars(self.additional_definitions)
        self.assert_var(self.another_string_var).is_equal_to(self.another_string_var_value)
        

    def test_variable_can_be_added(self):
        self.setup_additional_vars()
        self.manager.add(self.another_string_var, self.another_string_var_value)
        self.assert_var(self.another_string_var).is_equal_to(self.another_string_var_value)
        

    def test_returns_environment_variable_value(self):
        self.assert_var(self.environment_var).is_equal_to(self.environment_var_value)


    def test_envirionment_variables_override_defined_variables(self):
        self.manager.add(self.environment_var, 'different_value')
        self.assert_var(self.environment_var).is_equal_to(self.environment_var_value)


    def test_returns_resolved_variable_value(self):
        tokenized_var = 'TOKENIZED'
        tokenized_var_value = 'contains ${STRING_VAR}'
        expected_value = 'contains the string value'
        self.manager.add(tokenized_var, tokenized_var_value)
        self.assert_var(tokenized_var).is_equal_to(expected_value)


    def test_returns_same_string_if_embeded_variable_not_defined(self):
        no_resolution_string = 'contains ${UNDEFINED} variable'
        self.assert_resolved(no_resolution_string).is_equal_to(no_resolution_string)


    def test_returns_resolved_string_if_variable_is_defined(self):
        resolution_string = 'contains ${STRING_VAR}'
        expected_result = 'contains the string value'
        self.assert_resolved(resolution_string).is_equal_to(expected_result)


    def test_resolves_numeric_variables(self):
        resolution_string = 'contains ${INT_VAR}'
        expected_result = 'contains 1'
        self.assert_resolved(resolution_string).is_equal_to(expected_result)


    def test_resolves_multiple_embedded_variables(self):
        resolution_string = 'contains ${INT_VAR} and ${STRING_VAR}'
        expected_result = 'contains 1 and the string value'
        self.assert_resolved(resolution_string).is_equal_to(expected_result)


    def test_resolves_string_composed_of_other_variables_with_embedded_variables(self):
        resolution_string = 'contains ${COMPOSED_VAR}'
        expected_result = 'contains the string value and 1'
        self.assert_resolved(resolution_string).is_equal_to(expected_result)


    def test_returns_partial_resolved_string_if_contains_embedded_with_no_resolution(self):
        resolution_string = 'embedded: ${COMPOSED_NO_RESOLUTION}'
        expected_result = 'embedded: this has ${UNDEFINED}'
        self.assert_resolved(resolution_string).is_equal_to(expected_result)



    def assert_var(self, var_name):
        actual_value = self.manager.get(var_name)
        return assert_that(actual_value)


    def assert_resolved(self, to_resolve):
        actual_value = self.manager.resolve(to_resolve)
        return assert_that(actual_value)

    
    def setup_additional_vars(self):
        self.another_string_var = 'another_var'
        self.another_string_var_value = 'another_value'
        self.additional_definitions = {
            self.another_string_var: self.another_string_var_value
        }
        



if __name__=="__main__":
    unittest.main()