import pytest
from flask_jwt_extended import create_access_token

from main import create_app
from models.User import User
from resources.extensions import db


@pytest.fixture
def test_app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def auth_headers(test_app):
    with test_app.app_context():
        user = User(username="user", password_hash="password")
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=str(user.id))
        return {"Authorization": f"Bearer {access_token}"}
