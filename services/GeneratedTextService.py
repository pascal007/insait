from uuid import UUID
from marshmallow import ValidationError
from repository.GeneratedTextRepository import GeneratedTextRepository
from services.OpenAIStrategyService import OpenAIGPT4oMiniStrategy


class GeneratedTextManager:
    def __init__(self):
        self.strategy = OpenAIGPT4oMiniStrategy()
        self.repository = GeneratedTextRepository()

    def fetch_generated_text(self, user_id, prompt_id):
        user_id = UUID(user_id)
        generated_text = self.repository.get_by_id(user_id, prompt_id)
        if not generated_text:
            raise FileNotFoundError("Not found")
        return generated_text

    def delete_generated_text(self, user_id, prompt_id):
        user_id = UUID(user_id)
        self.repository.delete(user_id, prompt_id)

    def generate_and_store_text(self, user_id, prompt):
        user_id = UUID(user_id)
        response = self.strategy.generate_text(prompt)
        return self.repository.create(user_id, prompt, response)

    def update_generated_text(self, user_id, prompt_id, response):
        user_id = UUID(user_id)
        return self.repository.update(user_id, prompt_id, response)
