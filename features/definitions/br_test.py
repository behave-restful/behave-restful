"""
"""

vars = {
    'BR_TESTING_STATUS': 'running',
    'BASE_URL': 'http://my.server.com',
    'RESOURCE': 'resource',
    'OBJECT_ID': 3,
    'RESOURCE_NAME': 'resolved name'
}

def initialize_definition(context):
    context.vars.add_vars(vars)
