from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from logger_config import logger
from services.GeneratedTextService import GeneratedTextManager


class GeneratedTextResourceById(Resource):

    @jwt_required()
    def get(self, prompt_id):
        user_id = get_jwt_identity()
        logger.info(f"User {user_id} requested generated text with ID: {prompt_id}")

        try:
            generated_text_manager = GeneratedTextManager()
            generated_text = generated_text_manager.fetch_generated_text(user_id, prompt_id)
            logger.info(f"Successfully retrieved generated text {prompt_id} for user {user_id}.")
            return {"success": True, "data": generated_text.to_dict()}, 200

        except ValidationError as err:
            logger.warning(f"Validation error for user {user_id} on fetch: {err}")
            return {'success': False, 'error': err.messages}, 422

        except FileNotFoundError as err:
            logger.warning(f"Generated text {prompt_id} not found for user {user_id}: {err}")
            return {'success': False, 'error': str(err)}, 404

        except Exception as e:
            logger.error(f"Unexpected error while fetching text {prompt_id} for user {user_id}: {str(e)}",
                         exc_info=True)
            return {'success': False, 'error': 'Internal server error'}, 500

    @jwt_required()
    def delete(self, prompt_id):
        user_id = get_jwt_identity()
        logger.info(f"User {user_id} requested deletion of generated text with ID: {prompt_id}")

        try:
            generated_text_manager = GeneratedTextManager()
            generated_text_manager.delete_generated_text(user_id, prompt_id)
            logger.info(f"Successfully deleted generated text {prompt_id} for user {user_id}.")
            return {"success": True, "message": "Generated Text successfully deleted"}, 200

        except ValidationError as err:
            logger.warning(f"Validation error for user {user_id} on deletion: {err}")
            return {'success': False, 'error': err.messages}, 422

        except FileNotFoundError as err:
            logger.warning(f"Generated text {prompt_id} not found for user {user_id}: {err}")
            return {'success': False, 'error': str(err)}, 404

        except Exception as e:
            logger.error(f"Unexpected error while deleting text {prompt_id} for user {user_id}: {str(e)}",
                         exc_info=True)
            return {'success': False, 'error': 'Internal server error'}, 500

    @jwt_required()
    def put(self, prompt_id):
        user_id = get_jwt_identity()
        logger.info(f"User {user_id} requested update for generated text with ID: {prompt_id}")

        data = request.get_json()

        if not data or "response" not in data or not data["response"]:
            logger.warning(f"Update failed for user {user_id}: Missing response content.")
            return {"success": False, "error": "Content is required."}, 400

        generated_text_manager = GeneratedTextManager()

        try:
            updated_text = generated_text_manager.update_generated_text(user_id, prompt_id, data["response"])
            logger.info(f"Successfully updated generated text {prompt_id} for user {user_id}.")
            return {"success": True, "data": updated_text.to_dict()}, 200

        except ValidationError as err:
            logger.warning(f"Validation error for user {user_id} on update: {err}")
            return {"success": False, "error": str(err)}, 422

        except FileNotFoundError as err:
            logger.warning(f"Generated text {prompt_id} not found for user {user_id}: {err}")
            return {'success': False, 'error': str(err)}, 404

        except Exception as e:
            logger.error(f"Unexpected error while updating text {prompt_id} for user {user_id}: {str(e)}", exc_info=True)
            return {'success': False, 'error': 'Internal server error'}, 500


class GeneratedTextResource(Resource):

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        logger.info(f"User {user_id} requested text generation with data: {data}")

        if not data or "prompt" not in data or not data["prompt"]:
            logger.warning(f"User {user_id} submitted an invalid request: {data}")
            return {"success": False, "error": "Prompt is required."}, 422

        try:
            generated_text_manager = GeneratedTextManager()
            generated_text = generated_text_manager.generate_and_store_text(user_id, data["prompt"])
            logger.info(f"Generated text stored successfully for user {user_id}.")
            return {"success": True, "data": generated_text.to_dict()}, 201

        except ValidationError as err:
            logger.warning(f"Validation error for user {user_id}: {err}")
            return {'success': False, 'error': str(err)}, 422

        except Exception as e:
            logger.error(f"Unexpected error for user {user_id}: {str(e)}", exc_info=True)
            return {'success': False, 'error': 'Internal server error'}, 500
