#!/usr/bin/python3
"""This module defines an API for amenity objects in storage"""
from flask import abort, request, make_response, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def get_place_amenities(place_id):
    """
        This function returns a list of JSON representations of all
        amenity objects linked to the place specified by 'place_id'
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    ameinities = [amenity.to_dict() for amenity in place.amenities]
    return make_response(jsonify(amenities))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def remove_amenity(place_id, amenity_id):
    """This function unlinks an amenity object from a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity or amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def add_amenity(place_id, amenity_id):
    """This function links an amenity object to a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    place.amenities.append(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
