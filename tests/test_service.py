from uuid import UUID

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta


@patch("repository.UserRepository.UserRepository.create_user")
def test_create_user(mock_create_user, user_service):
    mock_create_user.return_value = {"id": 1, "username": "testuser"}

    user = user_service.create_user("testuser", "password")

    assert user == {"id": 1, "username": "testuser"}
    mock_create_user.assert_called_once_with("testuser", "password")


@patch("repository.UserRepository.UserRepository.verify_password")
@patch("jwt.encode")
def test_generate_token(mock_jwt_encode, mock_verify_password, user_service):
    mock_verify_password.return_value = MagicMock(id=1, username="testuser")

    mock_jwt_encode.return_value = "mocked_token"
    token = user_service.generate_token("testuser", "password")

    assert token == "mocked_token"
    mock_verify_password.assert_called_once_with("testuser", "password")
    mock_jwt_encode.assert_called_once_with(
        {
            "sub": "1",
            "username": "testuser",
            "exp": pytest.approx(datetime.utcnow() + timedelta(hours=24), abs=5)
        },
        user_service.secret_key,
        algorithm="HS256"
    )


@patch("repository.UserRepository.UserRepository.verify_password")
def test_generate_token_invalid_user(mock_verify_password, user_service):
    mock_verify_password.return_value = None

    with pytest.raises(FileNotFoundError, match="User does not exist"):
        user_service.generate_token("wronguser", "password")

    mock_verify_password.assert_called_once_with("wronguser", "password")


@patch("repository.GeneratedTextRepository.GeneratedTextRepository.get_by_id")
def test_fetch_generated_text(mock_get_by_id, manager):
    mock_get_by_id.return_value = {"id": UUID("123e4567-e89b-12d3-a456-426614174000"), "user_id": UUID("456e4567-e89b-12d3-a456-426614174111"), "prompt": "Test prompt", "response": "Generated text"}

    text = manager.fetch_generated_text("456e4567-e89b-12d3-a456-426614174111", "123e4567-e89b-12d3-a456-426614174000")

    assert text["prompt"] == "Test prompt"
    mock_get_by_id.assert_called_once()


@patch("repository.GeneratedTextRepository.GeneratedTextRepository.get_by_id")
def test_fetch_generated_text_not_found(mock_get_by_id, manager):
    mock_get_by_id.return_value = None

    with pytest.raises(FileNotFoundError, match="Not found"):
        manager.fetch_generated_text("456e4567-e89b-12d3-a456-426614174111", "123e4567-e89b-12d3-a456-426614174000")


@patch("repository.GeneratedTextRepository.GeneratedTextRepository.delete")
def test_delete_generated_text(mock_delete, manager):
    manager.delete_generated_text("456e4567-e89b-12d3-a456-426614174111", "123e4567-e89b-12d3-a456-426614174000")

    mock_delete.assert_called_once()


@patch("services.OpenAIStrategyService.OpenAIGPT4oMiniStrategy.generate_text")
@patch("repository.GeneratedTextRepository.GeneratedTextRepository.create")
def test_generate_and_store_text(mock_create, mock_generate_text, manager):
    mock_generate_text.return_value = "Generated response"
    mock_create.return_value = {"user_id": UUID("456e4567-e89b-12d3-a456-426614174111"), "prompt": "Test prompt", "response": "Generated response"}

    result = manager.generate_and_store_text("456e4567-e89b-12d3-a456-426614174111", "Test prompt")

    assert result["response"] == "Generated response"
    mock_generate_text.assert_called_once_with("Test prompt")
    mock_create.assert_called_once()


@patch("repository.GeneratedTextRepository.GeneratedTextRepository.update")
def test_update_generated_text(mock_update, manager):
    mock_update.return_value = {"user_id": UUID("456e4567-e89b-12d3-a456-426614174111"), "prompt_id": UUID("123e4567-e89b-12d3-a456-426614174000"), "response": "Updated response"}

    result = manager.update_generated_text("456e4567-e89b-12d3-a456-426614174111", "123e4567-e89b-12d3-a456-426614174000", "Updated response")

    assert result["response"] == "Updated response"
    mock_update.assert_called_once()


@patch("openai.ChatCompletion.create")
def test_generate_text(mock_openai_create, strategy):
    mock_openai_create.return_value = {
        "choices": [{"message": {"content": "Mocked response"}}]
    }

    prompt = "What is AI?"
    response = strategy.generate_text(prompt)

    assert response == "Mocked response"
    mock_openai_create.assert_called_once_with(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )