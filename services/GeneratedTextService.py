import os
from uuid import UUID

import openai
from marshmallow import ValidationError
from dotenv import load_dotenv

from models.GeneratedText import GeneratedText
from resources.extensions import db


load_dotenv()


class GeneratedTextManager:
    open_ai = openai

    def __init__(self):
        self.open_ai.api_key = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def fetch_generated_text(user_id, prompt_id):
        user_id = UUID(user_id)
        generated_text = GeneratedText.query.filter_by(
            user_id=user_id, id=prompt_id).first()
        if not generated_text:
            raise ValidationError("Generated Text not found")
        return generated_text

    @staticmethod
    def delete_generated_text(user_id, prompt_id):
        user_id = UUID(user_id)
        generated_text = GeneratedText.query.filter_by(
            user_id=user_id, id=prompt_id).first()
        if not generated_text:
            raise ValidationError("Generated Text not found")
        db.session.delete(generated_text)
        db.session.commit()

    def generate_and_store_text(self, user_id, prompt):
        user_id = UUID(user_id)
        response = self.open_ai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        generated_text_response = response["choices"][0]["message"]["content"]
        generated_text = GeneratedText(user_id=user_id, prompt=prompt, response=generated_text_response)
        db.session.add(generated_text)
        db.session.commit()
        return generated_text

    @staticmethod
    def update_generated_text(user_id, prompt_id, new_prompt):
        user_id = UUID(user_id)
        generated_text = GeneratedText.query.filter_by(user_id=user_id, id=prompt_id).first()
        if not generated_text:
            raise ValidationError("Generated Text not found")

        generated_text.prompt = new_prompt
        db.session.commit()
        return generated_text


