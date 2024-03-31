#!/usr/bin/python3
""" Create a flask web application API """

from flask import Flask
from flask import jsonify
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ Tearsdown app context """
    storage.close()


@app.errorhandler(404)
def error_not_found(error):
    """Handler for 404 errors that returns a JSON-formatted 404 status code"""
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = getenv("HBNB_API_PORT", '5000')
    app.run(host=host, port=port, threaded=True)
