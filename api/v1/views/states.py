#!/usr/bin/python3
""" View for State objects that handles all default RESTFul API actions """

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves the list of all State objects """
    list_of_states = []
    states = storage.all(State).values()
    for state in states:
        list_of_states.append(state.to_dict())
    return jsonify(list_of_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """ Retrieves a State object by ID """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """ Deletes a State object by ID """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a new State """
    json_state = request.get_json()
    if not json_state:
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    new_state = State(**json_state)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_by_id(state_id):
    """ Updates a State object by ID """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_state = request.get_json()
    if json_state is None:
        abort(400, 'Not a JSON')
    for key, value in json_state.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
