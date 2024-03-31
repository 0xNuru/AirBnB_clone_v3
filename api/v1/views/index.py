#!/usr/bin/python3
"""this module contains the index route"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns a JSON of ok"""
    return jsonify(status='OK')


@app_views.route('/stats')
def stats():
    """ Retrieves the number of each objects by type """
    classes = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(classes)
