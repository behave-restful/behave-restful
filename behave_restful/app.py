"""
Implements the Behave Restful application object which initializes the global
execution context providing access to directories and other services to 
simplify testing.  
"""
import os
import shutil

import requests

import behave_restful._definitions as _defs
import behave_restful._hooks as _hooks

from behave_restful._hooks import (
    BEFORE_ALL, 
    AFTER_ALL, 
    BEFORE_FEATURE, 
    AFTER_FEATURE, 
    BEFORE_SCENARIO, 
    AFTER_SCENARIO,
    BEFORE_STEP,
    AFTER_STEP,
    BEFORE_TAG,
    AFTER_TAG
)

class BehaveRestfulApp(object):
    """
    Behave Restful application class used to initialize the execution context
    for a test run.
    """

    def initialize_context(self, context, test_dir):
        """
        Initializes the provide context object exposing through it relevant
        directories and services. 

        :param context:
            A behave context object.
        :param test_dir:
            Directory where the tests are located. This is, usually, the 
            features folder of the test project.
        """
        context.test_dir = test_dir
        context.working_dir = os.getcwd()
        context.default_session = requests
        context.session = context.default_session
        _defs.DefinitionInitializer().initialize(context)
        _hooks.EnvironmentHookInitializer().initialize(context)



    
class BrInitApp(object):
    """
    Application class for the br-init command that creates a new Behave Restful
    project.
    """
    def __init__(self):
        self.project_dir = os.path.join(os.getcwd(), 'features')
        behave_restful_root = os.path.dirname(os.path.abspath(__file__))
        self.src_dir = os.path.join(behave_restful_root, '_project')


    def init_project(self, project_dir=None):
        """
        Creates a new project by copying the default template files to the
        specified destination, or the features folder in the current working
        directory.

        The destination folder cannot exist before running this application.
        """
        self.project_dir = project_dir or self.project_dir
        msg = 'Creating project at: {d}'.format(d=self.project_dir)
        print(msg)
        self._check_project_dir()
        self._copy_project_files()


    def _check_project_dir(self):
        if self._exists(self.project_dir):
            raise ProjectInitError('Target directory already exists')

    
    def _copy_project_files(self):
        self._copy_tree(self.src_dir, self.project_dir)


    def _exists(self, path):
        return os.path.exists(path)


    def _copy_tree(self, src, dst):
        shutil.copytree(src, dst)



class ProjectInitError(Exception):
    """
    """
    def __init__(self, reason):
        super(ProjectInitError, self).__init__()
        self.reason = reason


    def __repr__(self):
        return 'ProjectInitError({r})'.format(r=self.reason)
