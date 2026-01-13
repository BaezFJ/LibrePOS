import pytest

from librepos.app import create_app
from librepos.app.config import TestingConfig
from librepos.app.extensions import db


@pytest.fixture
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

    return app


@pytest.fixture
def client(app):
    return app.test_client()
