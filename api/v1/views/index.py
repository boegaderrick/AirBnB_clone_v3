#!/usr/bin/python3
"""This script defines a status function"""
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """This function shows the status of the API"""
    return {'status': 'OK'}


@app_views.route('/stats', methods=['GET'])
def stats():
    """This method retrieves object stats"""
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    objs = {}
    objs['amenities'] = storage.count(Amenity)
    objs['cities'] = storage.count(City)
    objs['places'] = storage.count(Place)
    objs['reviews'] = storage.count(Review)
    objs['states'] = storage.count(State)
    objs['users'] = storage.count(User)

    return objs
