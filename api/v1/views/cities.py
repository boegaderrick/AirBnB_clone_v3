#!/usr/bin/python3
"""This module defines an API for city objects in storage"""
from flask import abort, request, make_response, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """
        This function returns a list of JSON representations of all
        city objects linked to the city specified by 'state_id'
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in storage.all(City).values()
              if city.state_id == state.id]
    # cities = state.cities
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """
        This function returns a JSON represention of city object specified
        by 'city_id'. If no such object is found a '404' is raised.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """This function deletes a city object from storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """This function creates a city object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        request.get_json()
    except Exception:
        abort(400, description='Not a JSON')

    if not request.get_json():
        abort(400, description='Not a JSON')
    if not request.get_json().get('name'):
        abort(400, description='Missing name')

    properties = request.get_json()
    properties.update({'state_id': state.id})
    city = City(**properties)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """This function updates a city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        if not request.get_json():
            abort(400, description='Not a JSON')
    except Exception:
        abort(400, description='Not a JSON')

    updates = request.get_json()
    for key, value in updates.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at' and\
                key != 'state_id':
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
