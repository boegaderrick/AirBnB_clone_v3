#!/usr/bin/python3
"""This module launches a flask web app"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(Exception=None):
    """This function handles teardown"""
    storage.close()


if __name__ == '__main__':
    from os import getenv
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    host = host if host else '0.0.0.0'
    port = port if port else 5000
    app.run(host=host, port=port, threaded=True)
