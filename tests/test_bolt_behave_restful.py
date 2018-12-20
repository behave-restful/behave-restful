import unittest

from assertpy import assert_that
import bolt.api as bolt_api

import behave_restful.bolt_behave_restful as br_task


class TestRunBehaveTask(unittest.TestCase):

    def setUp(self):
        self.directory = '/location/of/features'
        self.options = {
            'junit': True
        }
        self.config = {
            'directory': self.directory,
            'options': self.options
        }
        self.task = RunBehaveRestfulTaskSpy()



    def test_raises_if_no_directory_specified(self):
        with self.assertRaises(bolt_api.RequiredConfigurationError):
            self.given({})


    def test_raises_if_specified_directory_does_not_exist(self):
        self.task.directory_exists_return = False
        with self.assertRaises(br_task.FeaturesDirectoryDoesNotExistError):
            self.given(self.config)


    def test_uses_specified_directory(self):
        self.given(self.config)
        assert_that(self.task.features_dir).is_equal_to(self.directory)


    def test_uses_specified_options(self):
        self.given(self.config)
        assert_that(self.task.options).is_same_as(self.options)


    def test_ignores_options_if_not_specified(self):
        self.given({'directory': self.directory})
        assert_that(self.task.invoked_arguments).is_equal_to([self.directory])


    def test_adds_feature_directory_as_the_last_parameter(self):
        self.given(self.config)
        assert_that(self.task.invoked_arguments).ends_with(self.directory)


    def test_passes_options_to_behave(self):
        self.given(self.config)
        assert_that(self.task.invoked_arguments).contains('--junit')


    def test_raises_failure_if_behave_fails(self):
        self.task.behave_result = 1
        with self.assertRaises(bolt_api.TaskFailedError):
            self.given(self.config)


    def given(self, configuration):
        self.task(config=configuration)
        return self



class RunBehaveRestfulTaskSpy(br_task.RunBehaveRestfulTask):
    def __init__(self):
        super(RunBehaveRestfulTaskSpy, self).__init__()
        self.directory_exists_return = True
        self.invoked_arguments = []
        self.behave_result = 0


    def _exists(self, path):
        return self.directory_exists_return


    def _invoke_behave(self, arguments):
        self.invoked_arguments = arguments
        return self.behave_result


    



class TestBehaveOptionsParser(unittest.TestCase):

    def setUp(self):
        self.parser = br_task.BehaveOptionsParser()

    def test_given_no_options_returns_empty_commandline_parameters(self):
        self.given({}).expect()


    def test_value_parameter_is_prefixed_and_returned_with_specified_value(self):
        expected_value = '/a/directory'
        options = {
            'junit-directory': expected_value
        }
        self.given(options).expect('--junit-directory', expected_value)


    def test_boolean_option_is_included_if_true(self):
        options = {
            'junit': True
        }
        self.given(options).expect('--junit')


    def test_boolean_options_is_negated_if_false(self):
        options = {
            'junit': False
        }
        self.given(options).expect('--no-junit')


    def test_show_option_is_included_if_true(self):
        options = {
            'show-source': True,
            'show-timings': True,
            'show-skipped': True,
        }
        self.given(options).expect('--show-source', '--show-timings', '--show-skipped')


    def test_show_option_is_correctly_negated_if_false(self):
        options = {
            'show-source': False,
            'show-timings': False,
            'show-skipped': False,
        }
        self.given(options).expect('--no-source', '--no-timings', '--no-skipped')


    def test_formats_defined_data(self):
        options = {
            'define': {
                'var1': 'val1',
                'var2': 'val2'
            }
        }
        self.given(options).expect('--define', 'var1=val1', '--define', 'var2=val2')


    def test_formats_tags_as_a_comma_delimited_list(self):
        options = {
            'tags': ['@t1', '@t2', '~@t3']
        }
        self.given(options).expect('--tags', '@t1,@t2,~@t3')


    def test_can_specify_multiple_tags_options_by_creating_list_of_lists(self):
        options = {
            'tags':[
                ['@t1', '~@t2'],
                ['~@t3', '@t4']
            ]
        }
        self.given(options).expect('--tags', '@t1,~@t2', '--tags', '~@t3,@t4')


    def given(self, options):
        self.options = options
        return self


    def expect(self, *args):
        self.parameters = self.parser.parse(self.options)
        if not args:
            assert_that(self.parameters).is_equal_to([])
        else:
            assert_that(self.parameters).contains(*args)
        return self
        



if __name__=="__main__":
    unittest.main()
