import openai
import os
from dotenv import load_dotenv

from interface.LLMStrategyInterface import LLMStrategy

load_dotenv()


class OpenAIGPT4oMiniStrategy(LLMStrategy):
    def __init__(self):
        self.client = openai
        self.client.api_key = os.getenv("OPENAI_API_KEY")

    def generate_text(self, prompt: str) -> str:
        response = self.client.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )["choices"][0]["message"]["content"]
        return response
