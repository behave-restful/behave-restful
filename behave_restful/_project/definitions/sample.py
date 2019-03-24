"""
This module is loaded when 'sample' is passed as the definition to Behave Restful.
The variables here defined can then be used for testing. Definitions are used
to define variables with values matching for different testing environments.
"""

vars = {
    'BASE_URL': 'https://api.github.com',
}

def initialize_definition(context):
    context.vars.add_vars(vars)
