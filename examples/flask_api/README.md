# Example: Test a Flask REST API End to End

## Setup

To work in a conda env, do:

```bash
conda create --name behave_restful_flask_api pip python=3.7 && \
    source activate behave_restful_flask_api && \
    pip install -r requirements.txt
```

## Running the Example

The aim is to have a runnable task that starts our Flask server, and then once the server is running, executes our behave tests.

In this example, we use [bolt](https://github.com/abantos/bolt/), which is a python task runner modelled after js grunt.

With your conda env activated (or otherwise making sure all requirements are in your python env), do

```bash
# shell in the root of flask_api example
bolt test-features
```

...if all goes well, this should
- start up the Flask server
- wait 2 seconds to make sure Flask started fully
- execute behave

...and you will see output like the below

```
 * Serving Flask app "api" (lazy loading)
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
Feature: Provides api info # features/provides_api_info.feature:1
  Requests to the root of the api
  provide infp about the api itself
  Scenario: Get the api version                           features/provides_api_info.feature:6
    Given a request url http://127.0.0.1:5000
    When the request sends GET                           # "GET / HTTP/1.1" 200 -
    Then the response status is OK                      
    And the response json matches                        
      """
      {
          "title": "APIInfoObject",
          "type": "object",
          "properties": {
              "version": {"type": "string"}
          },
          "required": ["version"]
      }
      """
    And the response json at $.version is equal to "1.0"

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
5 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.010s
```