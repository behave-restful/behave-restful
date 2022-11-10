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
    'NULL_LINK_PATH': "$.songs.[2].link",
    'LINK_PATH': "$.songs[0].link",
    'AVAILABLE_PATH': '$.songs[0].available',
    'NOT_AVAILABLE_PATH': '$.songs[2].available',
    'AVAILABLE_SONG_PATH': "$.SONGS.[2].available",
    'BOOK_INDEX': 1,
    'TITLE': 'title',
    'CATEGORY_FICTION': "fiction",
    'PARAM_ID': 'id_number',
    'PARAM_NAME': 'first_name',
    'TEST_SCHEMA_ID': 'TEST_SCHEMA',
    'KNOWN_BOOK_TITLE': 'The Lord of the Rings',
    'CONTENT_LENGTH_HEADER': 'Content-Length',
    'KEEP_ALIVE': 'keep-alive'
}

def initialize_definition(context):
    context.vars.add_vars(vars)
    context.vars.add('WORKING_DIR', context.working_dir)
