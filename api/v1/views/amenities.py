#!/usr/bin/python3
""" View for Amenities objects that handles all default RESTFul API actions """

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ Retrieves the list of all Amenity objects """
    list_of_amenities = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        list_of_amenities.append(amenity.to_dict())
    return jsonify(list_of_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """ Retrieves the list of Amenities by ID """
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """ Deletes the list of Amenities by ID """
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an Amenity """
    json_amenity = request.get_json()
    if json_amenity is None:
        abort(400, 'Not a JSON')
    if "name" not in json_amenity:
        abort(400, 'Missing name')
    if len(json_amenity) != 1:
        abort(400)
    new_amenity = Amenity(**json_amenity)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a amenity object """
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    json_amenity = request.get_json()
    if json_amenity is None:
        abort(400, 'Not a JSON')
    for key, value in json_amenity.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(amenities, key, value)
    storage.save()
    return jsonify(amenities.to_dict()), 200
