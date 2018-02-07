"""
"""
import os.path

import behave_restful._utils as _utils

HOOKS_DIR = 'hooks'
PYTHON_EXTENSION = '.py'

class EnvironmentHookInitializer(object):
    """
    """

    def initialize(self, context):
        context.hooks = EnvironmentHookManager()
        hooks_dir = os.path.join(context.test_dir, HOOKS_DIR)
        if self._hooks_dir_exists(hooks_dir):
            self._add_to_search_path(hooks_dir)
            self._register_modules(context.hooks, hooks_dir)
            



    def _add_to_search_path(self, *path_tokens):
        _utils.add_search_path(*path_tokens)


    def _register_modules(self, hooks_manager, hooks_dir):
        dir_contents = self._get_hooks_dir_content(hooks_dir)
        module_names = [self._get_module_name(f) for f in dir_contents]
        modules = [self._load_hook_module(m) for m in module_names if m]
        [hooks_manager.register_module(m) for m in modules]  



    def _hooks_dir_exists(self, path):
        return os.path.exists(path)


    def _get_hooks_dir_content(self, hooks_dir):
        return os.listdir(hooks_dir)


    def _get_module_name(self, file_name):
        name, extension = os.path.splitext(file_name)
        if extension == PYTHON_EXTENSION:
            return name


    def _load_hook_module(self, module_name):
        return _utils.load_module(module_name)





BEFORE_ALL = 'before_all'
AFTER_ALL = 'after_all'
BEFORE_FEATURE = 'before_feature'
AFTER_FEATURE = 'after_feature'
BEFORE_SCENARIO ='before_scenario'
AFTER_SCENARIO = 'after_scenario'
BEFORE_STEP = 'before_step'
AFTER_STEP = 'after_step'
BEFORE_TAG = 'before_tag'
AFTER_TAG = 'after_tag'

class EnvironmentHookManager(object):
    """
    """
    def __init__(self):
        self._registered_callbacks = {
            BEFORE_ALL: [],
            AFTER_ALL: [],
            BEFORE_FEATURE: [],
            AFTER_FEATURE: [],
            BEFORE_SCENARIO: [],
            AFTER_SCENARIO: [],
            BEFORE_STEP: [],
            AFTER_STEP: [],
            BEFORE_TAG: [],
            AFTER_TAG: []
        }
        
    
    def register_module(self, module):
        self._append_callback(BEFORE_ALL, module)
        self._append_callback(AFTER_ALL, module)
        self._append_callback(BEFORE_FEATURE, module)
        self._append_callback(AFTER_FEATURE, module)
        self._append_callback(BEFORE_SCENARIO, module)
        self._append_callback(AFTER_SCENARIO, module)
        self._append_callback(BEFORE_STEP, module)
        self._append_callback(AFTER_STEP, module)
        self._append_callback(BEFORE_TAG, module)
        self._append_callback(AFTER_TAG, module)



    def get_hooks(self, hook_type):
        return self._registered_callbacks.get(hook_type)


    def invoke(self, hook_type, context, *args):
        hooks = self.get_hooks(hook_type)
        [hook(context, *args) for hook in hooks]        
        


    def _append_callback(self, hook_name, module):
        if hasattr(module, hook_name):
            hook = getattr(module, hook_name)
            hook_collection = self.get_hooks(hook_name)
            hook_collection.append(hook)
            
