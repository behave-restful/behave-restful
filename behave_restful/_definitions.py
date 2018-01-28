"""
This module exposes functionality to handle definition files in the application.
"""
import os

import behave_restful._errors as _errors
import behave_restful._utils as _utils
import behave_restful.xpy as xpy

DEFINITIONS_DIR = 'definitions'
DEFINITION_KEY = 'definition'
class DefinitionInitializer(object):
    """
    Initializes definitions into the execution context.
    """
    
    def initialize(self, context):
        """
        Initializes the specified definition, if exists, into the execution
        context.

        :param context:
            Context object to initialize.
        """
        context.vars = VarsManager()
        self._add_to_search_path(context.test_dir, DEFINITIONS_DIR)
        if DEFINITION_KEY in context.config.userdata:
            self._initialize_definition(context)


    def _add_to_search_path(self, *path_tokens):
        _utils.add_search_path(*path_tokens)


    def _initialize_definition(self, context):
        definition_name = context.config.userdata[DEFINITION_KEY]
        definition_module = self._load_definition(definition_name)
        if not definition_module: raise DefinitionNotFoundError(definition_name)
        definition_module.initialize_definition(context)


    def _load_definition(self, definition_name):
        return _utils.load_module(definition_name)





VAR_PREFIX = '${'
VAR_SUFFIX = '}'

_NO_NEXT_VAR = None

class VarsManager(object):
    """
    Manages access and resolution of variables defined in definition files or
    in the environment.
    """
    def __init__(self):
        self._definitions = {}


    def add(self, var_name, var_value):
        """
        Adds a new variable. If the variable already existed, the value is
        overwritten.

        :param str var_name: 
            Name of the variable to add.
        :param var_value: 
            Value to set the variable to.
        :type var_value:
            any
        """
        self._definitions[var_name] = var_value


    def add_vars(self, definitions):
        """
        Adds all the variables specified in the definition. 
        
        The definition parameter must be a dictionary where the keys are used as 
        variable names and the values as the values for the variables. Existing 
        variables will be replaced.

        :param dict definitions:
            Dictionary containing the variable definitions.
        """
        self._definitions.update(definitions)


    def get(self, var_name, def_value=None):
        """
        Returns the resolved value of a variable.

        :param str var_name:
            Name of the variable to retrieve value.
        :param def_value:
            Optional default value to be returned if the variable is not 
            defined.

        :return:
            The resolved value of the variable.
        """
        environment_value = os.environ.get(var_name)
        value = environment_value or self._definitions.get(var_name, def_value)
        return self.resolve(value) if xpy.is_string(value) else value
        

    def resolve(self, to_resolve):
        """
        Resolves a string containing embedded variables.

        :param str to_resolve:
            String in which we want to resolve the embedded variables.
        
        :return:
            The string with embedded variables resolved or the same string if
            variable cannot be resolved or the string does not contain embedded
            variables.
        :rtype:
            str

        The following code sample shows how this function works:

        ..  code-block:: python

            variable_definitions = {
                'INT_VAR': 1,
                'STR_VAR': 'a string',
                'EMBEDDED_VARS': 'contains ${INT_VAR} and ${STR_VAR},
            }

            manager = VarsManager()
            manager.add_vars(variable_definitions)

            manager.resolve('contains ${INT_VAR}')
            # returns 'contains 1'

            manager.resolve('contains ${STR_VAR}')
            # returns 'contains a string'

            manager.resolve('contains ${INT_VAR} and ${STR_VAR}')
            # returns 'contains 1 and a string'

            manager.resolve('this ${EMBEDDED_VARS}')
            # returns 'this contains 1 and a string'

            manager.resolve('this is ${UNDEFINED}')
            # returns 'this is ${UNDEFINED}'
        """
        resolved = to_resolve
        next_var_name = self._find_var_name_in(resolved)
        while next_var_name:
            resolved, next_var_name = self._resolve_in(resolved, next_var_name)
        return resolved


    def _resolve_in(self, to_resolve, var_name):
        value = self.get(var_name)
        return self._do_resolve_in(to_resolve, var_name, value) if value is not None else (to_resolve, _NO_NEXT_VAR)


    def _do_resolve_in(self, to_resolve, var_name, value):
        resolved = self._replace_with(to_resolve, var_name, value)
        next_var_name = self._find_var_name_in(resolved)
        return resolved, next_var_name



    def _find_var_name_in(self, to_resolve):
        var_starts = to_resolve.find(VAR_PREFIX) + len(VAR_PREFIX)
        var_ends = to_resolve.find(VAR_SUFFIX, var_starts)
        return to_resolve[var_starts:var_ends]


    def _replace_with(self, to_resolve, var_name, value):
        token = ''.join([VAR_PREFIX, var_name, VAR_SUFFIX])
        return to_resolve.replace(token, str(value))



class DefinitionNotFoundError(_errors.BehaveRestfulException):
    """
    """
    def __init__(self, definition_name):
        self.definition_name = definition_name


    def __repr__(self):
        return "DefinitionNotFoundError(definition_name='{dn}')".format(dn=self.definition_name)


    
