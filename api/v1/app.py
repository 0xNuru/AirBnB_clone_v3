#!/usr/bin/python3
"""create a flask web application API"""
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
"""details of our env"""
host = getenv('HBNB_API_HOST', '0.0.0.0')
port = int(getenv('HBNB_API_PORT', '5000'))

app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': host}})


@app.teardown_appcontext
def teardown(exception):
    """tearsdown app context"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """Handles the 404 HTTP error code response"""
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
