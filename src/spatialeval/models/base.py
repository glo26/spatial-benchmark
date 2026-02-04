"""
Base class for LLM model wrappers.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseModel(ABC):
    """
    Abstract base class for LLM model wrappers.

    All model implementations should inherit from this class and implement
    the `generate` method.
    """

    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """
        Initialize the model wrapper.

        Args:
            model_name: The name/identifier of the model.
            api_key: The API key for authentication. If None, will look for
                     environment variables.
        """
        self.model_name = model_name
        self.api_key = api_key

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response for the given prompt.

        Args:
            prompt: The input prompt string.
            **kwargs: Additional generation parameters.

        Returns:
            The model's response string.
        """
        pass

    def __call__(self, prompt: str, **kwargs) -> str:
        """Allow the model to be called directly as a function."""
        return self.generate(prompt, **kwargs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model_name='{self.model_name}')"
