from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def api_info():
    """
    requests to the root of this api
    just return metadata about the api itself
    """
    return json.dumps({
        "version": "1.0"
    })