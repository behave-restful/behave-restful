from flask import Flask, jsonify, request
from PIL import Image


app = Flask(__name__)

@app.route('/ping')
def ping():
    """
    used by bolt task WaitForServerRunning 
    to poll/confirm when server has started
    """
    return jsonify({
        "status": 'ok'
    })

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    """
    take the user's name from either a query param
    or posted json and return a customized greeting
    """

    if request.method == 'GET':
        name = request.args['name']
    elif request.method == 'POST':
        content = request.get_json(silent=True)
        name = content['name']

    return jsonify({
        "greeting": 'hello, {}!'.format(name)
    })

@app.route('/measure_image', methods=['POST'])
def measure_image():
    """
    Accepts a posted image file and responds with that images dimensions.
    This obviously makes no sense in the real world,
    but it's an easy way to test that behave-restful posts files properly.
    """
    im_file = request.files['image']
    im = Image.open(im_file)
    return jsonify({
        'filename': im_file.filename,
        'width': im.size[0],
        'height': im.size[1]
    })