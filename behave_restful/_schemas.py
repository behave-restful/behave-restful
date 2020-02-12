"""
"""
import json
import os.path

import jsonref
import yaml

def add_json_schemas(schemas, context):
    """
    """
    if not hasattr(context, 'schemas') or not context.schemas:
        context.schemas = {}
    context.schemas.update(schemas)


def add_openapi_schemas(openapi_filename, context):
    abs_path = os.path.abspath(openapi_filename)
    root, filename = os.path.split(openapi_filename)
    loader = ReferenceFileLoader(root)
    reader = OpenApiReader(filename, loader)
    add_json_schemas(reader.schemas, context)


class OpenApiReader:
    def __init__(self, filename, loader):
        self._filename = filename
        self._loader = loader
        self._content = None


    @property
    def content(self):
        if not self._content:
            self._content = self._load()
        return self._content


    @property
    def schemas(self):
        return self.content.get('components').get('schemas')


    def _load(self):
        content = self._loader(self._filename)
        content = jsonref.JsonRef.replace_refs(content, loader=self._loader)
        return content





class ReferenceFileLoader:
    def __init__(self, root_dir):
        self.root_dir = root_dir

        
    def __call__(self, ref_file):
        full_name = os.path.join(self.root_dir, ref_file)
        reader = get_reader(ref_file)
        return self._load(reader, full_name)


    def _load(self, reader, filename):
        with open(filename) as fin:
            return reader.load(fin)


YAML_EXT = '.yaml'

def get_reader(filename):
    name, ext = os.path.splitext(filename)
    if ext == YAML_EXT:
        return yaml
    return json