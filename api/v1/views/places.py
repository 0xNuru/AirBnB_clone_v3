#!/usr/bin/python3
""" View for Place objects that handles all default RESTFul API actions """

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


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
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    required_fields = ['user_id', 'name']
    for field in required_fields:
        if field not in json_data:
            abort(400, f'Missing {field}')
    user_id = json_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    new_place = Place(city_id=city_id, **json_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    for key, value in json_data.items():
        if key not in ('id', 'user_id', 'city_id', 'created_at',
                       'updated_at'):
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
