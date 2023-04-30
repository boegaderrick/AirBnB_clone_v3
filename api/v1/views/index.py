#!/usr/bin/python3
"""This script defines a status function"""
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """This function shows the status of the API"""
    return {'status': 'OK'}
