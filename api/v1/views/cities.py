#!/usr/bin/python3
""" View for City objects that handles all default RESTFul API actions """

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views, storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities_by_states(state_id):
    """ Retrieves the list of all cities of a State """
    list_of_cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        list_of_cities.append(city.to_dict())
    return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """ Retrieves the list of cities by ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities_by_id(city_id):
    """ Deletes the list of cities by ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a city """
    json_city = request.get_json()
    if json_city is None:
        abort(400, 'Not a JSON')
    if "name" not in json_city:
        abort(400, 'Missing name')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_city['state_id'] = state_id
    new_city = City(**json_city)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_state(city_id):
    """ Updates a city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_city = request.get_json()
    if json_city is None:
        abort(400, 'Not a JSON')
    for key, value in json_city.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
