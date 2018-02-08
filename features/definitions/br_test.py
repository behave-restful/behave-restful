"""
"""

vars = {
    'BR_TESTING_STATUS': 'running',
    'BASE_URL': 'http://my.server.com',
    'RESOURCE': 'resource',
    'OBJECT_ID': 3,
    'RESOURCE_NAME': 'resolved name',
    'TYPE_STRING': '{"type": "string"}',
    'TYPE_NUMBER': '{"type": "number"}',
    'REQUIRED': 'required'
}

def initialize_definition(context):
    context.vars.add_vars(vars)
