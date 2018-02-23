"""
Initializes the defined schemas.
"""


SCHEMAS = {
    'TEST_SCHEMA': {
        "title": "SampleObject",
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"}
        },
        "required": ["id", "name"]
    }
}

SCHEMA_TESTING_FEATURES = {'step then the response json matches defined schema'}

def before_feature(context, feature):
    if feature.name.lower() in SCHEMA_TESTING_FEATURES:
        context.schemas = SCHEMAS


def after_feature(context, feature):
     if feature.name.lower() in SCHEMA_TESTING_FEATURES:
         context.schemas = None