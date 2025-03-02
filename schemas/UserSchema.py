from marshmallow import Schema, fields, validate


class UserAccessSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=5))
    password = fields.String(required=True, validate=validate.Length(min=5))

