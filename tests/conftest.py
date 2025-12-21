import pytest

from librepos.app import create_app
from librepos.extensions import db


@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

    return app


@pytest.fixture
def client(app):
    return app.test_client()
