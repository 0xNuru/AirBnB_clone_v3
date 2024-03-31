#!/usr/bin/python3
""" View for Review objects that handles all default RESTFul API actions """

from flask import jsonify
from flask import abort
from flask import request
from api.v1.views import app_views, storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews_by_place(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a Review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_review = request.get_json()
    if not json_review:
        abort(400, description='Not a JSON')
    if 'user_id' not in json_review:
        abort(400, description='Missing user_id')
    user_id = json_review['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in json_review:
        abort(400, description='Missing text')
    new_review = Review(place_id=place_id, **json_review)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    json_review = request.get_json()
    if not json_review:
        abort(400, description='Not a JSON')
    for key, value in json_review.items():
        if key not in ('id', 'user_id', 'place_id', 'created_at',
                       'updated_at'):
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
