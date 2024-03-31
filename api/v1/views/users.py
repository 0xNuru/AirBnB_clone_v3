#!/usr/bin/python3
""" View for User objects that handles all default RESTFul API actions """

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves the list of all User objects """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in json_data:
            abort(400, f'Missing {field}')
    new_user = User(**json_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    for key, value in json_data.items():
        if key not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
