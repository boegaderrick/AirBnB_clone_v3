#!/usr/bin/python3
"""This module defines an API for place objects in storage"""
from flask import abort, request, make_response, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """
        This function returns a list of JSON representations of all
        place objects linked to the place specified by 'city_id'
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in storage.all(Place).values()
              if place.city_id == city.id]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """
        This function returns a JSON represention of place object specified
        by 'place_id'. If no such object is found a '404' is raised.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """This function deletes a place object from storage"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """This function creates a place object"""
    city = storage.get(City, city_id)
    if not city:
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
    if not request.get_json().get('name'):
        abort(400, description='Missing name')

    properties = request.get_json()
    properties.update({'city_id': city.id})
    place = Place(**properties)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """This function updates a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        if not request.get_json():
            abort(400, description='Not a JSON')
    except Exception:
        abort(400, description='Not a JSON')

    updates = request.get_json()
    for key, value in updates.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at' and\
                key != 'city_id' and key != 'user_id':
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)