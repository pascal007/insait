from uuid import uuid4

import pytest
from flask_jwt_extended import create_access_token

from main import create_app
from models.User import User
from repository.GeneratedTextRepository import GeneratedTextRepository
from repository.UserRepository import UserRepository
from resources.extensions import db
from services.GeneratedTextService import GeneratedTextManager
from services.OpenAIStrategyService import OpenAIGPT4oMiniStrategy
from services.UserService import UserService


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


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def sample_prompt():
    return "Sample test prompt"


@pytest.fixture
def sample_response():
    return "Sample generated response"


@pytest.fixture
def generated_text(test_app, user_id, sample_prompt, sample_response):
    instance = GeneratedTextRepository.create(user_id, sample_prompt, sample_response)
    yield instance
    db.session.delete(instance)
    db.session.commit()


@pytest.fixture
def test_user(test_app, user_repo):
    with test_app.app_context():
        return user_repo.create_user("test_user", "securepassword")


@pytest.fixture
def user_repo():
    return UserRepository()


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def manager():
    return GeneratedTextManager()


@pytest.fixture
def strategy():
    return OpenAIGPT4oMiniStrategy()