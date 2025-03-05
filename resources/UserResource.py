from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from schemas.UserSchema import UserSignUpSchema, UserAccessSchema
from services.UserService import UserService

from logger_config import logger


class CreateUserResource(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        try:
            validated_data = UserSignUpSchema().load(data)
            user_service = UserService()
            user_service.create_user(validated_data['username'].lower().strip(), validated_data['password'])
            logger.info(f"User registered successfully: {validated_data['username']}")
            return {'success': True, 'message': 'User registered successfully'}, 201
        except ValidationError as err:
            logger.warning(f"Validation error on user creation: {err.messages}")
            return {'success': False, 'error': err.messages}, 422
        except Exception as e:
            logger.error(f"Unexpected error during user registration: {str(e)}")
            return {'success': False, 'error': 'Internal server error'}, 500


class LoginUserResource(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        try:
            validated_data = UserAccessSchema().load(data)
            user_service = UserService()
            token = user_service.generate_token(
                validated_data['username'].lower().strip(), validated_data['password'])
            if not token:
                logger.warning(f"Invalid login attempt: {validated_data['username']}")
                return {'success': False, 'message': 'Invalid credentials'}, 401
            return {'success': True, 'data': token}, 200
        except ValidationError as err:
            logger.warning(f"Validation error on login: {err.messages}")
            return {'success': False, 'error': err.messages}, 422
        except FileNotFoundError as e:
            logger.warning(f"Validation error on login: User not found")
            return {'success': False, 'error': 'User does not exist'}, 404
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            return {'success': False, 'error': 'Internal server error'}, 500
