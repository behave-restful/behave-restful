import os.path
import unittest

from assertpy import assert_that

import behave_restful._hooks as _hooks


class TestEnvironmentHookInitializer(unittest.TestCase):

    def setUp(self):
        self.context_mock = self
        self.test_dir = 'the_test_dir'
        self.expected_search_path = os.path.join(self.test_dir, 'hooks')
        self.initializer = EnvironmentHookInitializerSpy()


    def test_creates_environment_hook_manager_in_context(self):
        self.initializer.initialize(self.context_mock)
        assert_that(self.context_mock.hooks).is_instance_of(_hooks.EnvironmentHookManager)


    def test_adds_hooks_directory_to_the_search_path(self):
        self.initializer.initialize(self.context_mock)
        assert_that(self.initializer.added_search_path).is_equal_to(self.expected_search_path)


    def test_retrieves_python_modules_from_hooks_dir_if_exists(self):
        self.initializer.initialize(self.context_mock)
        assert_that(self.initializer.list_dir_invoked).is_true()


    def test_loads_all_modules_in_directory(self):
        self.initializer.initialize(self.context_mock)
        assert_that(self.initializer.hook_modules).contains('a')
        assert_that(self.initializer.hook_modules).contains('b')
        assert_that(self.initializer.hook_modules).does_not_contain('c')
        assert_that(self.initializer.hook_modules).does_not_contain('d')
        assert_that(self.initializer.hook_modules).does_not_contain(None)

    




class EnvironmentHookInitializerSpy(_hooks.EnvironmentHookInitializer):
    def __init__(self):
        self.added_search_path = None
        self.hooks_directory_exists = True
        self.list_dir_invoked = False
        self.hook_modules = []


    def _add_to_search_path(self, *path_tokens):
        self.added_search_path = os.path.join(*path_tokens)


    def _hooks_dir_exists(self, path):
        return self.hooks_directory_exists


    def _get_hooks_dir_content(self, path):
        self.list_dir_invoked = True
        return ['a.py', 'b.py', 'c.txt', 'd', '__pycache__']


    def _load_hook_module(self, module_name):
        self.hook_modules.append(module_name)
        return self





class TestEnvironmentHookManager(unittest.TestCase):

    def setUp(self):
        super(TestEnvironmentHookManager, self).setUp()
        self.manager = _hooks.EnvironmentHookManager()

    def test_registers_hooks_from_module(self):
        self.given(ModuleDouble())
        self.expect_hook_count(_hooks.BEFORE_ALL, 1)
        self.expect_hook_count(_hooks.AFTER_ALL, 1)
        self.expect_hook_count(_hooks.BEFORE_FEATURE, 1)
        self.expect_hook_count(_hooks.AFTER_FEATURE, 1)
        self.expect_hook_count(_hooks.BEFORE_SCENARIO, 1)
        self.expect_hook_count(_hooks.AFTER_SCENARIO, 1)
        self.expect_hook_count(_hooks.BEFORE_STEP, 1)
        self.expect_hook_count(_hooks.AFTER_STEP, 1)
        self.expect_hook_count(_hooks.BEFORE_TAG, 1)
        self.expect_hook_count(_hooks.AFTER_TAG, 1)


    def test_skips_hooks_not_defined_in_module(self):
        self.given(ModuleDummy())
        self.expect_hook_count(_hooks.BEFORE_ALL,0)
        self.expect_hook_count(_hooks.AFTER_ALL, 0)
        self.expect_hook_count(_hooks.BEFORE_FEATURE, 0)
        self.expect_hook_count(_hooks.AFTER_FEATURE, 0)
        self.expect_hook_count(_hooks.BEFORE_SCENARIO, 0)
        self.expect_hook_count(_hooks.AFTER_SCENARIO, 0)
        self.expect_hook_count(_hooks.BEFORE_STEP, 0)
        self.expect_hook_count(_hooks.AFTER_STEP, 0)
        self.expect_hook_count(_hooks.BEFORE_TAG, 0)
        self.expect_hook_count(_hooks.AFTER_TAG, 0)


    def test_invokes_specified_hook(self):
        self.given(ModuleDouble()).invoke(_hooks.BEFORE_ALL, 'context')
        assert_that(self.module.before_all_invoked).is_true()
        assert_that(self.module.specified_context).is_equal_to('context')


    def test_invokes_hook_with_specified_args(self):
        self.given(ModuleDouble()).invoke(_hooks.AFTER_FEATURE, 'context', 'the_feature')
        assert_that(self.module.after_feature_invoked).is_true()
        assert_that(self.module.specified_feture).is_equal_to('the_feature')


    def test_invokes_all_hooks_registered(self):
        module1 = ModuleDouble()
        self.manager.register_module(module1)
        module2 = ModuleDouble()
        self.manager.register_module(module2)
        self.manager.invoke(_hooks.BEFORE_SCENARIO, 'context', 'the_scenario')
        assert_that(module1.before_scenario_invoked).is_true()
        assert_that(module2.before_scenario_invoked).is_true()

    def test_propagates_exceptions(self):
        module = ModuleDouble()
        module.raise_exception = True
        self.given(module)
        with self.assertRaises(ValueError):
            self.invoke(_hooks.BEFORE_ALL, 'context')
                

    def given(self, module):
        self.module = module
        self.manager.register_module(self.module)
        return self


    def expect_hook_count(self, hook_name, expected_count):
        hooks = self.manager.get_hooks(hook_name)
        actual_count = len(hooks)
        assert_that(actual_count).is_equal_to(expected_count)
        return self


    def invoke(self, hook_type, *args):
        self.manager.invoke(hook_type, *args)





class ModuleDouble(object):
    def __init__(self):
        self.before_all_invoked = False
        self.after_all_invoked = False
        self.before_feature_invoked = False
        self.after_feature_invoked = False
        self.before_scenario_invoked = False
        self.after_scenario_invoked = False
        self.before_step_invoked = False
        self.after_step_invoked = False
        self.before_tag_invoked = False
        self.after_tag_invoked = False
        self.specified_context = None
        self.specified_feture = None
        self.raise_exception = False


    def before_all(self, context):
        if self.raise_exception: raise ValueError('Forced')
        self.specified_context = context
        self.before_all_invoked = True

    def after_all(self, context):
        self.after_all_invoked = True

    def before_feature(self, context, feature):
        self.before_feature_invoked = True

    def after_feature(self, context, feature):
        self.specified_feture = feature
        self.after_feature_invoked = True

    def before_scenario(self, context, scenario):
        self.before_scenario_invoked = True

    def after_scenario(self, context, scenario):
        self.after_scenario_invoked = True

    def before_step(self, context, step):
        self.before_step_invoked = True

    def after_step(self, context, step):
        self.after_step_invoked = True

    def before_tag(self, context, tag):
        self.before_tag_invoked = True

    def after_tag(self, context, tag):
        self.after_tag_invoked = True


class ModuleDummy(object): pass


# before_all(context)
# before_feature(context, feature)
# before_scenario(context, scenario)
# before_step(context, step)
# before_tag(context, tag)

if __name__=="__main__":
    unittest.main()