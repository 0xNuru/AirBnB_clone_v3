#!/usr/bin/python3
"""this module contains the index route"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns a JSON of ok"""
    return jsonify(status='OK')
