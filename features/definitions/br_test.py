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
    'REQUIRED': 'required',
    'TITLE_PATH': '$.store.book[3].title',
    'BOOK_INDEX': 1,
    'TITLE': 'title',
    'CATEGORY_FICTION': "fiction",
    'PARAM_ID': 'id_number',
    'PARAM_NAME': 'first_name',
    'TEST_SCHEMA_ID': 'TEST_SCHEMA'
}

def initialize_definition(context):
    context.vars.add_vars(vars)
