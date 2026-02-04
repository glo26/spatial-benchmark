"""
Anthropic model wrapper for SpatialEval.
"""

import os
from typing import Optional

from spatialops.models.base import BaseModel


class AnthropicModel(BaseModel):
    """
    Wrapper for Anthropic models (Claude 3, etc.).

    Example:
        >>> model = AnthropicModel(model_name="claude-3-opus-20240229")
        >>> response = model.generate("What is 2 + 2?")
    """

    def __init__(
        self,
        model_name: str = "claude-3-opus-20240229",
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: int = 2048,
    ):
        """
        Initialize the Anthropic model wrapper.

        Args:
            model_name: The Anthropic model identifier.
            api_key: The Anthropic API key. If None, uses ANTHROPIC_API_KEY env var.
            temperature: Sampling temperature (0.0 for deterministic).
            max_tokens: Maximum tokens in the response.
        """
        super().__init__(model_name, api_key)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = None

    @property
    def client(self):
        """Lazy initialization of the Anthropic client."""
        if self._client is None:
            try:
                import anthropic
            except ImportError:
                raise ImportError(
                    "Anthropic package not installed. Install with: pip install anthropic"
                )

            api_key = self.api_key or os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "Anthropic API key not provided. Set ANTHROPIC_API_KEY environment variable "
                    "or pass api_key to the constructor."
                )
            self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response using the Anthropic API.

        Args:
            prompt: The input prompt.
            **kwargs: Additional parameters to pass to the API.

        Returns:
            The model's response string.
        """
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)

        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            system="You are a helpful assistant specialized in spatial reasoning. "
            "Solve the given problem step by step and provide a clear final answer.",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text
