import os

import behave_restful.app as br_app


def before_all(context):
    this_directory = os.path.abspath(os.path.dirname(__file__))
    br_app.BehaveRestfulApp().initialize_context(context, this_directory)