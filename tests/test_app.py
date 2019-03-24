import os
import unittest

from assertpy import assert_that
import requests

import behave_restful.app as br_app

class TestBehaveRestfulApp(unittest.TestCase):

    def setUp(self):
        self.test_dir = '/a/path'
        self.context = ContextDouble()
        self.app = br_app.BehaveRestfulApp()
        self.app.initialize_context(self.context, self.test_dir)


    def test_context_is_initialized_with_test_dir(self):
        assert_that(self.context.test_dir).is_equal_to(self.test_dir)


    def test_context_is_initialized_with_current_working_dir(self):
        assert_that(self.context.working_dir, os.getcwd())


    def test_context_default_session_is_initialized_with_requests_module(self):
        assert_that(self.context.default_session).is_same_as(requests)


    def test_sets_the_session_to_the_default_session(self):
        assert_that(self.context.session).is_same_as(self.context.default_session)



class ContextDouble(object):
    def __init__(self):
        self.config = self
        self.userdata = {}



class TestBrInitApp(unittest.TestCase):

    def setUp(self):
        self.app = BrInitAppSpy()
        self.default_directory = os.path.join(os.getcwd(), 'features')
        self.another_directory = os.path.join(os.getcwd(), 'another')
        self.project_source = os.path.join(os.getcwd(), 'behave_restful', '_project')

    def test_initializes_directory_to_features_in_current_folder(self):
        assert_that(self.app.project_dir).is_equal_to(self.default_directory)


    def test_replaces_project_directory_with_specified_directory(self):
        self.app.init_project(self.another_directory)
        assert_that(self.app.project_dir).is_equal_to(self.another_directory)


    def test_keeps_default_project_directory_if_none_specified(self):
        self.app.init_project()
        assert_that(self.app.project_dir).is_equal_to(self.default_directory)


    def test_initializes_the_project_source_files_location(self):
        assert_that(self.app.src_dir).is_equal_to(self.project_source)


    def test_raises_if_directory_already_exists(self):
        self.app.return_destination_exists = True
        assert_that(self.app.init_project).raises(br_app.ProjectInitError).when_called_with()


    def test_copies_project_files_to_target_directory(self):
        self.app.init_project()
        assert_that(self.app.specified_src, self.app.src_dir)
        assert_that(self.app.specified_dst, self.app.project_dir)

class BrInitAppSpy(br_app.BrInitApp):
    def __init__(self):
        super().__init__()
        self.return_destination_exists = False
        self.specified_src = None
        self.specified_dst = None


    def _exists(self, path):
        return self.return_destination_exists


    def _copy_tree(self, src, dst):
        self.specified_src = src
        self.specified_dst = dst





if __name__=="__main__":
    unittest.main()