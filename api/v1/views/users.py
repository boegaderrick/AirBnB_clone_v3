#!/usr/bin/python3
"""This module defines an API for user objects in storage"""
from flask import abort, request, make_response, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """
        This function returns a list of JSON representations of all
        user objects in storage
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """
        This function returns a JSON represention of user object specified
        by 'user_id'. If no such object is found a '404' is raised.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """This function deletes a user object from storage"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """This function creates a user object"""
    try:
        request.get_json()
    except Exception:
        abort(400, description='Not a JSON')

    if not request.get_json():
        abort(400, description='Not a JSON')
    if not request.get_json().get('email'):
        abort(400, description='Missing email')
    if not request.get_json().get('password'):
        abort(400, description='Missing password')

    properties = request.get_json()

    user = User(**properties)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """This function updates a user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        if not request.get_json():
            abort(400, description='Not a JSON')
    except Exception:
        abort(400, description='Not a JSON')

    updates = request.get_json()
    for key, value in updates.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at' and\
                key != 'email':
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
