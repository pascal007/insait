from marshmallow import ValidationError

from models.User import User
from werkzeug.security import generate_password_hash, check_password_hash

from resources.extensions import db


class UserRepository:
    def __init__(self):
        self.db_session = db.session

    def create_user(self, username: str, password: str):
        if self.get_user_by_username(username):
            raise ValidationError("Username already taken")
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def get_user_by_username(self, username: str):
        return self.db_session.query(User).filter_by(username=username).first()

    def verify_password(self, username: str, password: str):
        user = self.get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
