import pytest
from flask import Flask
from flask.testing import FlaskClient
import sys
sys.path.append('c:/Users/nicole/PycharmProjects/dierban/game')
from runserver import bp


@pytest.fixture
def client() -> FlaskClient:
    app: Flask = Flask(__name__)
    app.register_blueprint(bp)
    client: FlaskClient = app.test_client()
    return client