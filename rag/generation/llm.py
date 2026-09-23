import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"


class OllamaLLM:
    """Generate responses using a local Ollama model."""

    def __init__(
        self,
        model_name: str = MODEL_NAME,
    ) -> None:
        self.model_name = model_name

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from the Ollama model.

        Args:
            prompt: Prompt sent to the LLM.

        Returns:
            Generated text response.
        """

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"].strip()
