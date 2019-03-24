"""
This module implements a bolt task that allows to execute feature tests using
behave. This task works with any behave project and also with Behave Restful
projects.

Additionally as a convenience, this module includes a second bolt task,
which allows you to wait for a server to start by polling a url
(waiting for OK response)
"""
import os.path
import requests
import subprocess
import time

import behave.__main__ as behave_main
import bolt.api as bolt_api


class RunBehaveRestfulTask(bolt_api.Task):
    """
    Bolt task that allows executing Behave Restful through bolt.
    """

    def _configure(self):
        self.features_dir = self._require('directory')
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
        if result != 0: raise bolt_api.TaskFailedError()


    def _exists(self, path):
        return os.path.exists(path)


    def _invoke_behave(self, arguments):
        return behave_main.main(arguments)


class WaitForServerRunning(bolt_api.Task):
    """
    Bolt task waits for a server to be ready
    by polling a provided url.

    The motivating case is end-to-end testing
    a REST API where we want to execute a 'behave-restful' task
    to test features but must wait first for a server to finish starting.

    For servers with very short start times, 
    it's usually fine to just add a 'sleep' task for a couple of seconds.
    But for servers with longer and/or unpredictable start times,
    it's better to wait only as long as really necessary.
    A common example would be an api that uses an AI classifier 
    and loads/inits a large model at startup time.

    Config:
        url: (string) url to poll for server readiness. 
            When GET url returns a 200 status, 
            the server is considered ready, 
            and this task completes successfully.

        [delay]: (float) a duration in seconds
            to wait before polling the url the first time.
            Default is 0 seconds.

        [interval]: (float) the interval in seconds to wait
            between polling requests to the url.
            Default 0.3 seconds

        [timeout]: (float) the max seconds to wait
            for the server to start.
            Will raise a TimeoutError if the url
            does not return a 200 response before this duration.
            Default 5 seconds
    """
    def __init__(self):
        super(WaitForServerRunning, self).__init__()
        self.process = None

    def tear_down(self):
        if self.process:
            self._terminate(self.process)
            
    def _configure(self):
        self.url = self.config.get('url')
        self.delay = self.config.get('delay') or 0
        self.interval = self.config.get('interval') or 0.3
        self.timeout = self.config.get('timeout') or 5

        if not self.url: raise UrlNotSpecifiedError()

    def _execute(self):
        if self.delay > 0:
            time.sleep(self.delay)

        timeout_time = time.time() + self.timeout
        while True:
            if time.time() > timeout_time:
                raise TimeoutError() 
            try:
                req = requests.request('GET', self.url)
                if(req.ok):
                    return
            except:
                time.sleep(self.interval)

        

    def _popen_script(self, args):
        return subprocess.Popen(args)

    def _terminate(self, process):
        process.terminate()
        
        
def register_tasks(registry):
    registry.register_task('behave-restful', RunBehaveRestfulTask())
    registry.register_task('wait-for-server-running', WaitForServerRunning())


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



class FeaturesDirectoryDoesNotExistError(bolt_api.ConfigurationValueError):
    """
    Exception class raised when the specified features directory does not
    exist.
    """
    def __init__(self, specified_directory):
        super(FeaturesDirectoryDoesNotExistError, self).__init__('directory', specified_directory)
        
        
class TimeoutError(bolt_api.TaskError):
    def __init__(self):
        super(TimeoutError, self).__init__()

class UrlNotSpecifiedError(bolt_api.RequiredConfigurationError):
    def __init__(self):
        super(UrlNotSpecifiedError, self).__init__('url')