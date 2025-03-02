from flask_restful import Resource
from flask import request
from marshmallow import ValidationError

from schemas.UserSchema import UserAccessSchema
from services.UserService import UserService


class CreateUserResource(Resource):

    @staticmethod
    def post():
        data = request.get_json()
        try:
            validated_data = UserAccessSchema().load(data)
            user_service = UserService()
            user_service.create_user(validated_data['username'], validated_data['password'])
            return {'success': True, 'message': 'User registered successfully'}, 201
        except ValidationError as err:
            return {'success': False, 'error': err.messages}, 400


class LoginUserResource(Resource):

    @staticmethod
    def post():
        data = request.get_json()
        try:
            validated_data = UserAccessSchema().load(data)
            user_service = UserService()
            token = user_service.generate_token(validated_data['username'], validated_data['password'])
            return {'success': True, 'data': token}, 200
        except ValidationError as err:
            return {'success': False, 'error': err.messages}, 400
