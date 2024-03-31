#!/usr/bin/python3
""" View for User objects that handles all default RESTFul API actions """

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves the list of all User objects """
    list_of_users = []
    users = storage.all(User).values()
    for user in users:
        list_of_users.append(user.to_dict())
    return jsonify(list_of_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    return jsonify(users.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    storage.delete(users)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User """
    json_user = request.get_json()
    if not json_user:
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    new_user = User(**json_user)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    json_user = request.get_json()
    if json_user is None:
        abort(400, 'Not a JSON')
    for key, value in json_user.items():
        if key not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(users, key, value)
    storage.save()
    return jsonify(users.to_dict()), 200
