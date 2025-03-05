import jwt
import os
from datetime import datetime, timedelta

from repository.UserRepository import UserRepository
from logger_config import logger


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.secret_key = os.getenv("JWT_SECRET_KEY")

    def create_user(self, username: str, password: str):
        try:
            logger.info(f"Creating user: {username}")
            return self.user_repo.create_user(username.lower().strip(), password)
        except Exception as e:
            logger.error(f"Error creating user {username}: {str(e)}")
            raise

    def generate_token(self, username: str, password: str):
        logger.debug(f"Attempting login for user: {username}")
        user = self.user_repo.verify_password(username, password)
        if not user:
            logger.warning(f"Invalid login attempt for username: {username}")
            raise FileNotFoundError("User does not exist")

        payload = {
            "sub": str(user.id),
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        logger.info(f"Token generated successfully for user: {username}")
        return token
