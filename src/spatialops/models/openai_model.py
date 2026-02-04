"""
OpenAI model wrapper for SpatialEval.
"""

import os
from typing import Optional

from spatialops.models.base import BaseModel


class OpenAIModel(BaseModel):
    """
    Wrapper for OpenAI models (GPT-4, GPT-5.2, etc.).

    Example:
        >>> model = OpenAIModel(model_name="gpt-5.2")
        >>> response = model.generate("What is 2 + 2?")
    """

    def __init__(
        self,
        model_name: str = "gpt-5.2",
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ):
        """
        Initialize the OpenAI model wrapper.

        Args:
            model_name: The OpenAI model identifier.
            api_key: The OpenAI API key. If None, uses OPENAI_API_KEY env var.
            temperature: Sampling temperature (0.0 for deterministic).
            max_tokens: Maximum tokens in the response.
        """
        super().__init__(model_name, api_key)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = None

    @property
    def client(self):
        """Lazy initialization of the OpenAI client."""
        if self._client is None:
            try:
                from openai import OpenAI
            except ImportError:
                raise ImportError(
                    "OpenAI package not installed. Install with: pip install openai"
                )

            api_key = self.api_key or os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OpenAI API key not provided. Set OPENAI_API_KEY environment variable "
                    "or pass api_key to the constructor."
                )
            self._client = OpenAI(api_key=api_key)
        return self._client

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response using the OpenAI API.

        Args:
            prompt: The input prompt.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            The model's response string.
        """
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant specialized in spatial reasoning. "
                    "Solve the given problem step by step and provide a clear final answer.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content
