#!/usr/bin/python3
""" View for Place objects that handles all default RESTFul API actions """

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views, storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    list_of_places = []
    for place in city.places:
        list_of_places.append(place.to_dict())
    return jsonify(list_of_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_place = request.get_json()
    if not json_place:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_place:
        abort(400, 'Missing user_id')
    user_id = json_place['user_id']
    if storage.get(User, user_id) is None:
        abort(404)
    if 'name' not in json_place:
        abort(400, 'Missing name')
    json_place['city_id'] = city_id
    new_place = Place(**json_place)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_place = request.get_json()
    if not json_place:
        abort(400, 'Not a JSON')
    for key, value in json_place.items():
        if key not in ('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
