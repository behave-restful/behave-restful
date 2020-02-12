"""
Initializes the defined schemas.
"""
import behave_restful.tools as brt

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
        brt.add_json_schemas(SCHEMAS, context)


def after_feature(context, feature):
     if feature.name.lower() in SCHEMA_TESTING_FEATURES:
         context.schemas = None