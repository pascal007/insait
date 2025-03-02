from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from services.GeneratedTextService import GeneratedTextManager


class GeneratedTextResourceById(Resource):

    @jwt_required()
    def get(self, prompt_id):
        user_id = get_jwt_identity()
        try:
            generated_text_manager = GeneratedTextManager()
            generated_text = generated_text_manager.fetch_generated_text(user_id, prompt_id)
            return {"success": True, "data": generated_text.to_dict()}, 200
        except ValidationError as err:
            return {'success': False, 'error': err.messages}, 404

    @jwt_required()
    def delete(self, prompt_id):
        user_id = get_jwt_identity()
        try:
            generated_text_manager = GeneratedTextManager()
            generated_text_manager.delete_generated_text(user_id, prompt_id)
            return {"success": True, "message": "Generated Text successfully deleted"}, 200
        except ValidationError as err:
            return {'success': False, 'error': err.messages}, 400

    @jwt_required()
    def put(self, prompt_id):
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data or "response" not in data or not data["response"]:
            return {"success": False, "error": "Content is required."}, 400

        try:
            updated_text = GeneratedTextManager.update_generated_text(user_id, prompt_id, data["response"])
            return {"success": True, "data": updated_text.to_dict()}, 200
        except ValidationError as err:
            return {"success": False, "error": str(err)}, 404


class GeneratedTextResource(Resource):

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data or "prompt" not in data or not data["prompt"]:
            return {"success": False, "error": "Prompt is required."}, 400

        try:
            generated_text_manager = GeneratedTextManager()
            generated_text = generated_text_manager.generate_and_store_text(user_id, data["prompt"])
            return {"success": True, "data": generated_text.to_dict()}, 201
        except Exception as err:
            return {'success': False, 'error': str(err)}, 400
