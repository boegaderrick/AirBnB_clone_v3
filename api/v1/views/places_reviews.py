#!/usr/bin/python3
"""This module defines an API for review objects in storage"""
from flask import abort, request, make_response, jsonify
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """
        This function returns a list of JSON representations of all
        review objects linked to the review specified by 'place_id'
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [review.to_dict() for review in storage.all(Review).values()
               if review.place_id == place.id]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """
        This function returns a JSON represention of review object specified
        by 'review_id'. If no such object is found a '404' is raised.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """This function deletes a review object from storage"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """This function creates a review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        request.get_json()
    except Exception:
        abort(400, description='Not a JSON')

    if not request.get_json():
        abort(400, description='Not a JSON')

    user_id = request.get_json().get('user_id')
    if not user_id:
        abort(400, description='Missing user_id')

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json().get('text'):
        abort(400, description='Missing text')

    properties = request.get_json()
    properties.update({'place_id': place.id})
    review = Review(**properties)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """This function updates a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    try:
        if not request.get_json():
            abort(400, description='Not a JSON')
    except Exception:
        abort(400, description='Not a JSON')

    updates = request.get_json()
    for key, value in updates.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at' and\
                key != 'place_id' and key != 'user_id':
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
