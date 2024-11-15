from google.generativeai.types.content_types import ContentsType
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from .base_prompt_class import BasePrompt
from utils.logging_config import log_execution
from typing import Optional, Union

class WasteDetection(BasePrompt):
    PROMPT = "Przeanalizuj dostarczony obraz i zidentyfikuj każde wyraźnie widoczne przedmioty. Jeśli można określić materiał lub przeznaczenie przedmiotu (np. 'plastikowa butelka na wodę', 'kartonowe opakowanie na jedzenie'), podaj tę informację. Jeśli tylko ogólny typ przedmiotu jest widoczny, ale nie można określić materiału ani konkretnego zastosowania, użyj ogólnej nazwy (np. 'butelka', 'pudełko'). Pomijaj elementy tła, które nie mają związku z analizą. Jeśli przedmiot jest nieczytelny lub niejasny, oznacz go jako 'Niezidentyfikowany'. Zwróć wszystkie zidentyfikowane przedmioty w formacie: 'element1, element2, element3' itd."
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash") -> None:
        super().__init__(api_key, model, self.PROMPT)

    @log_execution
    async def generate_response(self, user_input) -> Optional[str]:
        if self.api_client and self.api_client.model_instance:
            response = await self.api_client.model_instance.generate_content_async([
                {
                                "mime_type": "image/webp",
                                "data": user_input
                            }
            ], safety_settings={
                                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                                })
            return response.text.rstrip()
        else:
            return None
