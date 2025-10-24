import pytest

from librepos.main.app import create_app
from librepos.main.extensions import db


@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
