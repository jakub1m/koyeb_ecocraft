from typing import Union, Optional
from utils.api_client import GeminiApi
from utils.logging_config import log_execution

class BasePrompt:
    """
    Base class for interacting with the Gemini API, designed for generating
    responses based on a given prompt. Intended for subclassing to allow
    custom prompts, models, or handling of various input types.

    Attributes:
        api_key (str): The API key used to authenticate with the Gemini API.
        model (str): The name of the model to be used (default is "gemini-1.5-flash").
        PROMPT (str): The system prompt providing context for the model.
    """

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", prompt: str = "") -> None:
        """
        Initializes a BasePrompt instance with a specific API key, model name, and prompt.
        This can be overridden in subclasses to adapt the model or prompt behavior
        to specific requirements.

        Args:
            api_key (str): The API key for authentication.
            model (str): The model name to use with the Gemini API (default is "gemini-1.5-flash").
            prompt (str): The prompt to set as the system context for the model.
        """
        self.api_key = api_key
        self.model = model
        self.PROMPT = prompt
        self._init_model()

    @log_execution
    def _init_model(self) -> None:
        """
        Initializes the API client with the specified API key, model, and prompt.

        Can be overridden in subclasses if specialized behavior is needed
        during model or API client initialization.
        """
        self.api_client = GeminiApi(
            api_key=self.api_key,
            model=self.model,
            system_prompt=self.PROMPT
        )

    @log_execution
    async def generate_response(self, user_input) -> Optional[str]:
        """
        Generates a response based on user input using the model instance.

        Can be overridden in subclasses to handle other types of input,
        such as images or audio.

        Args:
            user_input (str): The text input provided by the user for generating a response.

        Returns:
            Optional[str]: The generated response text from the model or None if the
            model instance is unavailable.
        """
        if self.api_client and self.api_client.model_instance:
                response = await self.api_client.model_instance.generate_content_async(user_input)
                return response.text

        else:
            return None
