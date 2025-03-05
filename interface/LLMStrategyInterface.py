from abc import ABC, abstractmethod


class LLMStrategy(ABC):

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass
