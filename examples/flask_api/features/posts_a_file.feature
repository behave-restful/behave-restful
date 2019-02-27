Feature: Posts files as multipart data

  Demos sending a POST request that includes a file
  posted as multipart form data using behave-restful

Scenario: POSTs an image file
        Given a request url http://127.0.0.1:5000/measure_image
            And a request file payload
                | param | filename      | file                              | content_type  |
                | image | ok_16x16.bmp  | features/resources/ok_16x16.bmp   | image/bmp     |
        When the request sends POST
        Then the response status is OK
            And the response json matches
                """
                {
                    "title": "MeasureImageResponse",
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "width": {"type": "number"},
                        "height": {"type": "number"}
                    },
                    "required": ["filename", "width", "height"]
                }
                """
            And the response json at $.filename is equal to "ok_16x16.bmp"
            And the response json at $.width is equal to 16
            And the response json at $.height is equal to 16