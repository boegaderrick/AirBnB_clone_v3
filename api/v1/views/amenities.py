#!/usr/bin/python3
"""This module defines an API for amenity objects in storage"""
from flask import abort, request, make_response, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """
        This function returns a list of JSON representations of all
        amenity objects in storage
    """
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id):
    """
        This function returns a JSON represention of amenity object specified
        by 'amenity_id'. If no such object is found a '404' is raised.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """This function deletes a amenity object from storage"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """This function creates a amenity object"""
    try:
        request.get_json()
    except Exception:
        abort(400, description='Not a JSON')

    if not request.get_json():
        abort(400, description='Not a JSON')
    if not request.get_json().get('name'):
        abort(400, description='Missing name')

    amenity = Amenity(name=request.get_json().get('name'))
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """This function updates a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        if not request.get_json():
            abort(400, description='Not a JSON')
    except Exception:
        abort(400, description='Not a JSON')

    updates = request.get_json()
    for key, value in updates.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
