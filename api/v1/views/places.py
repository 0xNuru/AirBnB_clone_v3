#!/usr/bin/python3
""" View for Place objects that handles all default RESTFul API actions """

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views, storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    list_of_places = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
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
    json_place = request.get_json()
    if json_place is None:
        abort(400, description='Not a JSON')
    if not storage.get("User", json_place["user_id"]):
        abort(404, description='User not found')
    if not storage.get("City", city_id):
        abort(404, description='City not found')
    if "user_id" not in json_place:
        abort(400, description='Missing user_id')
    if "name" not in json_place:
        abort(400, description='Missing name')
    json_place["city_id"] = city_id
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
    if json_place is None:
        abort(400, description='Not a JSON')
    for key, value in json_place.items():
        if key not in ('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
