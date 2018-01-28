"""
This module implements a bolt task that allows to execute feature tests using
behave. This task works with any behave project and also with Behave Restful
projects.
"""
import os.path

import behave.__main__ as behave_main
import bolt.errors as bolt_errors


class RunBehaveRestfulTask(object):
    """
    Bolt task that allows executing Behave Restful through bolt.
    """

    def __call__(self, **kwargs):
        self.config = kwargs.get('config')
        self._configure()
        self._execute()


    def _configure(self):
        self.features_dir = self.config.get('directory')
        if not self.features_dir:
            raise FeaturesDirectoryNotSpecifiedError()
        if not self._exists(self.features_dir): 
            raise FeaturesDirectoryDoesNotExistError(self.features_dir)
        self.definition = self.config.get('definition')
        self.options = self.config.get('options') or {}


    def _execute(self):
        options_parser = BehaveOptionsParser()
        arguments = options_parser.parse(self.options)
        if self.definition:
            arguments.extend(['-D', 'definition={d}'.format(d=self.definition)])
        arguments.append(self.features_dir)
        result = self._invoke_behave(arguments)
        if result != 0: raise FeatureTestsFailedError()


    def _exists(self, path):
        return os.path.exists(path)


    def _invoke_behave(self, arguments):
        return behave_main.main(arguments)


def register_tasks(registry):
    registry.register_task('behave-restful', RunBehaveRestfulTask())


OPTION_PREFIX = '--{o}'
NEGATED_OPTION_PREFIX = '--no-{o}'

SHOW_OPTIONS = (
    'show-source',
    'show-timings', 
    'show-skipped'
)
SHOW_PREFIX = 'show'
NEGATED_SHOW_PREFIX = 'no'

DEFINED_DATA_OPTION = 'define'
DEFINED_DATA_FORMAT = '{k}={v}'

TAGS_OPTION = 'tags'
TAGS_DELIMITER = ','

class BehaveOptionsParser(object):
    """
    Parser class that knows how to convert options specified as a dictionary
    to a list of arguments that behave will understand.
    """

    def parse(self, options):
        """
        Parses the specified options returning a list of arguments that can be
        used to invoke behave.

        :param options:
            Dictionary containing the options to be used as arguments to behave.
        """
        parsed = []
        [parsed.extend(self._parse_option(option, value)) for option, value in options.items()]
        return parsed


    def _parse_option(self, option, value):
        formatting_function = self._get_formatting_function(option, value)
        return formatting_function(option, value)


    def _get_formatting_function(self, option, value):
        if self._is_bool(value):
            return self._format_bool
        if self._is_defined_data(option):
            return self._format_defined_data
        if self._is_tags_option(option):
            return self._format_tags
        return self._format_standard
        


    def _format_standard(self, option, value):
        prefixed_option = OPTION_PREFIX.format(o=option)
        return [prefixed_option, value]


    def _is_bool(self, value):
        return isinstance(value, bool)


    def _format_bool(self, option, value):
        if self._is_special_bool(option):
            prefixed_bool = self._format_special_bool(option, value)
        else:
            prefix = OPTION_PREFIX if value else NEGATED_OPTION_PREFIX
            prefixed_bool = prefix.format(o=option)
        return [prefixed_bool]


    def _is_special_bool(self, option):
        return option in SHOW_OPTIONS


    def _format_special_bool(self, option, value):
        if value:
            return OPTION_PREFIX.format(o=option)
        else:
            option = option.replace(SHOW_PREFIX, NEGATED_SHOW_PREFIX)
            return OPTION_PREFIX.format(o=option)


    def _is_defined_data(self, option):
        return option == DEFINED_DATA_OPTION


    def _format_defined_data(self, option, value):
        prefixed_option = OPTION_PREFIX.format(o=option)
        result = []
        for var, val in value.items():
            formatted_value = DEFINED_DATA_FORMAT.format(k=var, v=val)
            result.append(prefixed_option)
            result.append(formatted_value)
        return result


    def _is_tags_option(self, option):
        return option == TAGS_OPTION


    def _format_tags(self, option, value):
        formatted_result = []
        if self._has_multiple_tags_specified(value):
            [formatted_result.extend(entry) for entry in self._format_all_tags(option, value)]
        else:
            formatted_result.extend(self._format_one_tag(option, value))
        return formatted_result


    def _has_multiple_tags_specified(self, value):
        first_item = value[0]
        return isinstance(first_item, list)


    def _format_all_tags(self, option, entries):
        for tag_entry in entries:
            yield self._format_tags(option, tag_entry)


    def _format_one_tag(self, option, value):
        prefixed_option = OPTION_PREFIX.format(o=option)
        formatted_tags = TAGS_DELIMITER.join(value)
        return [prefixed_option, formatted_tags]




class FeaturesDirectoryNotSpecifiedError(bolt_errors.RequiredParameterMissingError):
    """
    Exception class raised when the directory with the feature tests is not
    specified.
    """
    def __init__(self):
        super(FeaturesDirectoryNotSpecifiedError, self).__init__('directory')



class FeaturesDirectoryDoesNotExistError(bolt_errors.ConfigurationValueError):
    """
    Exception class raised when the specified features directory does not
    exist.
    """
    def __init__(self, specified_directory):
        super(FeaturesDirectoryDoesNotExistError, self).__init__('directory', specified_directory)


class FeatureTestsFailedError(bolt_errors.TaskError):
    """
    Raised when behave fails.
    """
    pass
