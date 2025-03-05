from uuid import uuid4

import pytest
from marshmallow import ValidationError
from werkzeug.security import check_password_hash

from repository.GeneratedTextRepository import GeneratedTextRepository


def test_create_generated_text(test_app, user_id, sample_prompt, sample_response):
    generated_text = GeneratedTextRepository.create(user_id, sample_prompt, sample_response)
    assert generated_text is not None
    assert generated_text.user_id == user_id
    assert generated_text.prompt == sample_prompt
    assert generated_text.response == sample_response


def test_get_by_id(test_app, generated_text):
    retrieved_text = GeneratedTextRepository.get_by_id(generated_text.user_id, generated_text.id)
    assert retrieved_text is not None
    assert retrieved_text.id == generated_text.id


def test_update_generated_text(test_app, generated_text):
    updated_response = "Updated response text"
    updated_text = GeneratedTextRepository.update(generated_text.user_id, generated_text.id, updated_response)
    assert updated_text.response == updated_response


def test_update_non_existent_text(test_app, user_id):
    non_existent_id = uuid4()
    with pytest.raises(FileNotFoundError):
        GeneratedTextRepository.update(user_id, non_existent_id, "Updated response")


def test_delete_generated_text(test_app, generated_text):
    GeneratedTextRepository.delete(generated_text.user_id, generated_text.id)
    assert GeneratedTextRepository.get_by_id(generated_text.user_id, generated_text.id) is None


def test_delete_non_existent_text(test_app, user_id):
    non_existent_id = uuid4()
    with pytest.raises(ValidationError):
        GeneratedTextRepository.delete(user_id, non_existent_id)


def test_create_user(test_app, user_repo):
    with test_app.app_context():
        user = user_repo.create_user("new_user", "password123")
        assert user is not None
        assert user.username == "new_user"
        assert check_password_hash(user.password_hash, "password123")


def test_create_existing_user(test_app, user_repo, test_user):
    with test_app.app_context():
        with pytest.raises(ValidationError, match="Username already taken"):
            user_repo.create_user("test_user", "anotherpassword")


def test_get_user_by_username(test_app, user_repo, test_user):
    with test_app.app_context():
        user = user_repo.get_user_by_username("test_user")
        assert user is not None
        assert user.username == "test_user"


def test_verify_password_success(test_app, user_repo, test_user):
    with test_app.app_context():
        user = user_repo.verify_password("test_user", "securepassword")
        assert user is not None
        assert user.username == "test_user"


def test_verify_password_failure(test_app, user_repo, test_user):
    with test_app.app_context():
        user = user_repo.verify_password("test_user", "wrongpassword")
        assert user is None


def test_verify_password_nonexistent_user(test_app, user_repo):
    with test_app.app_context():
        user = user_repo.verify_password("unknown_user", "password")
        assert user is None
