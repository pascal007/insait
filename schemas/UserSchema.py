import re

from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSignUpSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @validates("username")
    def validate_username(self, value):
        if not re.match(r"^[a-zA-Z0-9_.-]+$", value):
            raise ValidationError("Username can only contain letters, numbers, dots, hyphens, and underscores.")

    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")


class UserAccessSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=5))
    password = fields.String(required=True, validate=validate.Length(min=5))