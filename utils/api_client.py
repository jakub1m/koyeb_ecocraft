from utils.logging_config import log_execution, logger
import google.generativeai as genai
import logging

class GeminiApi:
    """
    Class to interact with the Gemini API using a specified Generative AI model.

    This class provides functionality to initialize and configure a generative AI model
    from the Gemini API, and is designed for flexible interaction with various models
    supported by Gemini.
    """

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", system_prompt: str = "") -> None:
        """
        Initializes the GeminiApi class with the specified API key, model, and optional system prompt.

        Args:
            api_key (str): The API key for authenticating with the Gemini API service.
            model (str): The name of the model to use for generating responses.
                         Defaults to "gemini-1.5-flash".
            system_prompt (str): Optional system prompt to provide context or behavior
                                 guidelines for the model's responses. Defaults to an empty string.

        Attributes:
            model (str): Stores the model name.
            system_prompt (str): Stores the system prompt.
            model_instance (GenerativeModel or None): Holds the initialized model instance if
                                                     successfully created.
        """
        self.model = model
        self.system_prompt = system_prompt
        self.model_instance = None
        self._init_model(api_key, system_prompt)

    @log_execution
    def _init_model(self, api_key: str, system_prompt: str) -> None:
        """
        Configures the Gemini API and initializes the specified generative model instance.

        This method sets up the model instance using the provided API key and system prompt.
        It ensures proper configuration by logging any errors encountered during initialization.

        Args:
            api_key (str): The API key for authenticating requests with the Gemini API.
            system_prompt (str): The system prompt to guide the model's responses.

        Raises:
            Exception: If the model instance fails to initialize, the exception is logged
                       and re-raised for visibility in calling code.
        """
        try:
            genai.configure(api_key = api_key)

            self.model_instance = genai.GenerativeModel(
                model_name= self.model,
                system_instruction = self.system_prompt,
            )

            if not self.model_instance:
                logger.warning("Model instance was not initialized correctly.")
            else:
                logger.info(f"Model '{self.model}' initialized successfully.")

        except Exception as e:
            logger.error("Failed to initialize the model instance", exc_info=True)
            raise e
