from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from models.User import User
from resources.extensions import db


class UserService:

    def create_user(self, username, password):
        self.username_check(username)
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def username_check(username, exists=False):
        existing_user = User.query.filter_by(username=username).first()
        if exists:
            if not existing_user:
                raise ValidationError("Invalid username submitted")
            return existing_user
        if existing_user:
            raise ValidationError("Username is already used by another user")

    def generate_token(self, username, password):
        user = self.username_check(username, True)
        if not check_password_hash(user.password_hash, password):
            raise ValidationError("Invalid password submitted")
        return create_access_token(identity=user.id)

