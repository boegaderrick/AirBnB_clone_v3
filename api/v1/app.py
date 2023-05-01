#!/usr/bin/python3
"""This module launches a flask web app"""
from flask import Flask, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(Exception=None):
    """This function handles teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """This function handles '404' errors"""
    return make_response({'error': 'Not found'}, 404)


@app.errorhandler(400)
def bad_request(err):
    """This function handles '400' errors"""
    desc = err.description if err.description else err
    return make_response({'error': desc}, 400)


if __name__ == '__main__':
    from os import getenv
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    host = host if host else '0.0.0.0'
    port = port if port else 5000
    app.run(host=host, port=port, threaded=True)
