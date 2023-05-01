#!/usr/bin/python3
"""This module defines an API for state objects in storage"""
from flask import abort, request, make_response, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """
        This function returns a list of JSON representations of all
        state objects in storage
    """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """
        This function returns a JSON represention of state object specified
        by 'state_id'. If no such object is found a '404' is raised.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """This function deletes a state object from storage"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """This function creates a state object"""
    try:
        request.get_json()
    except Exception:
        abort(400, description='Not a JSON')

    if not request.get_json():
        abort(400, description='Not a JSON')
    if not request.get_json().get('name'):
        abort(400, description='Missing name')

    state = State(name=request.get_json().get('name'))
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """This function updates a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        if not request.get_json():
            abort(400, description='Not a JSON')
    except Exception:
        abort(400, description='Not a JSON')

    updates = request.get_json()
    for key, value in updates.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
