""" View objects that handles all default RESTFul API actions """

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews_by_place(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
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
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_data:
        abort(400, 'Missing user_id')
    user_id = json_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in json_data:
        abort(400, 'Missing text')
    new_review = Review(place_id=place_id, **json_data)
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
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    for key, value in json_data.items():
        if key not in ('id', 'user_id', 'place_id', 'created_at',
                       'updated_at'):
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
