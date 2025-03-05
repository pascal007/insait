from uuid import UUID
from models.GeneratedText import GeneratedText
from resources.extensions import db
from marshmallow import ValidationError


class GeneratedTextRepository:
    @staticmethod
    def get_by_id(user_id: UUID, prompt_id: UUID):
        return GeneratedText.query.filter_by(user_id=user_id, id=prompt_id).first()

    @staticmethod
    def create(user_id: UUID, prompt: str, response: str):
        generated_text = GeneratedText(user_id=user_id, prompt=prompt, response=response)
        db.session.add(generated_text)
        db.session.commit()
        return generated_text

    @staticmethod
    def update(user_id: UUID, prompt_id: UUID, response: str):
        generated_text = GeneratedTextRepository.get_by_id(user_id, prompt_id)
        if not generated_text:
            raise FileNotFoundError("Generated Text not found")
        generated_text.response = response
        db.session.commit()
        return generated_text

    @staticmethod
    def delete(user_id: UUID, prompt_id: UUID):
        generated_text = GeneratedTextRepository.get_by_id(user_id, prompt_id)
        if not generated_text:
            raise ValidationError("Generated Text not found")

        db.session.delete(generated_text)
        db.session.commit()
