import io
import json
import os.path
import unittest

import yaml
import jsonpath as jp

from assertpy import assert_that

import behave_restful._schemas as brs


class TestAddJsonSchemas(unittest.TestCase):

    def setUp(self):
        self.context = ContextDouble()
        self.schemas = {
            'person': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'}
                }
            }
        }
        brs.add_json_schemas(self.schemas, self.context)


    def test_sets_specified_schemas_in_context_object(self):
        
        assert_that(self.context.schemas).is_equal_to(self.schemas)


    def test_aggregates_schemas_as_they_are_specified(self):
        aggregate_schema = {
            'pet': {
                'type': 'object',
                'properties': {
                    'nickname': {'type': 'string'}
                }
            }
        }
        brs.add_json_schemas(aggregate_schema, self.context)
        assert_that(self.context.schemas).contains_key('person')
        assert_that(self.context.schemas).contains_key('pet')



class TestOpenApiReader(unittest.TestCase):

    def setUp(self):
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.filename = 'openapi.json'
        self.loader = ReferenceFileLoaderSpy(self.root)
        self.reader = brs.OpenApiReader(self.filename, self.loader)


    def test_returns_file_content(self):
        actual_value = self.get_from(self.reader.content, '$.openapi')
        assert_that(actual_value).is_equal_to('3.0.1')


    def test_returns_file_schemas(self):
        actual_value = self.get_from(self.reader.schemas, '$.NewSong.type')
        assert_that(actual_value).is_equal_to('object')


    def test_resolves_references(self):
        actual_value = self.get_from(self.reader.schemas, '$.NewSong.properties.artist.type')
        assert_that(actual_value).is_equal_to('object')


    def get_from(self, content, jpath):
        values = jp.jsonpath(content, jpath)
        return values[0]



        



class TestReferenceFileLoader(unittest.TestCase):
    
    def setUp(self):
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.loader = ReferenceFileLoaderSpy(self.root)


    def test_loads_specified_file_with_correct_reader(self):
        filename = 'openapi.yaml'
        self.loader(filename)
        assert_that(self.loader.specified_reader).is_same_as(yaml)


    def test_loads_absolute_path_to_specified_file_name(self):
        filename = 'openapi.json'
        expected_file = os.path.join(self.root, filename)
        self.loader(filename)
        assert_that(self.loader.specified_file).is_equal_to(expected_file)
        


class TestGetReader(unittest.TestCase):

    def test_returns_json_module_if_file_is_json(self):
        self.given('file.json').expect(json)


    def test_returns_yaml_module_if_file_is_yaml(self):
        self.given('file.yaml').expect(yaml)


    def given(self, filename):
        self.filename = filename
        return self

    def expect(self, expected):
        actual = brs.get_reader(self.filename)
        assert_that(actual).is_same_as(expected)
        return self



class ReferenceFileLoaderSpy(brs.ReferenceFileLoader):

    def _load(self, reader, filename):
        self.specified_reader = reader
        self.specified_file = filename
        if 'openapi' in filename:
            return FILE_CONTENT
        else:
            return REFERENCE_FILE_CONTENT




class ContextDouble:
    def __init__(self):
        self.schemas = None


FILE_CONTENT = {
    "openapi": "3.0.1",
    "info": {
      "title": "YAML Test Service Documentation",
      "description": "YAML file to test schema initialization through OpenAPI documents.",
      "version": "1.0",
      "contact": {
        "name": "Abantos"
      }
    },
    "servers": [
      {
        "url": "http://localhost:8080",
        "description": "Local server"
      }
    ],
    "tags": [
      {
        "name": "songs",
        "description": "Song management endpoints."
      }
    ],
    "paths": {
      "/songs": {
        "get": {
          "tags": [
            "songs"
          ],
          "summary": "Get songs collections.",
          "description": "Get the collection of songs stored in the service.",
          "responses": {
            "200": {
              "description": "OK",
              "content": {
                "application/json": {
                  "schema": {
                    "$ref": "#/components/schemas/SongCollection"
                  }
                }
              }
            }
          }
        }
      }
    },
    "components": {
      "schemas": {
        "NewSong": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string",
              "example": "Telegraph Road"
            },
            "artist": {
              "$ref": "models/artists.json#/components/schemas/Artist"
            }
          },
          "required": [
            "title"
          ]
        },
        "Song": {
          "type": "object",
          "allOf": [
            {
              "$ref": "#/components/schemas/NewSong"
            }
          ],
          "properties": {
            "id": {
              "type": "string",
              "example": "123456"
            }
          },
          "required": [
            "id",
            "title",
            "artist"
          ]
        },
        "SongCollection": {
          "type": "object",
          "properties": {
            "items": {
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/Song"
              }
            }
          }
        }
      }
    }
  }

REFERENCE_FILE_CONTENT = {
    "components": {
      "schemas": {
        "Artist": {
          "type": "object",
          "properties": {
            "name": {
              "type": "string",
              "example": "Dire Straits"
            }
          }
        }
      }
    }
  }
        



if __name__=="__main__":
    unittest.main()
