from google.generativeai.types.content_types import ContentsType
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from .base_prompt_class import BasePrompt
from utils.logging_config import log_execution
from typing import Optional, Union

class RecyclingGuide2(BasePrompt):
    PROMPT = """Przeanalizuj dostarczony obraz i zidentyfikuj każde wyraźnie widoczne przedmioty. Jeśli można określić materiał lub przeznaczenie przedmiotu (np. 'plastikowa butelka na wodę', 'kartonowe opakowanie na jedzenie'), podaj tę informację. Jeśli tylko ogólny typ przedmiotu jest widoczny, ale nie można określić materiału ani konkretnego zastosowania, użyj ogólnej nazwy (np. 'butelka', 'pudełko'). Pomijaj elementy tła, które nie mają związku z analizą. Jeśli przedmiot jest nieczytelny lub niejasny, oznacz go jako 'Niezidentyfikowany'. Dla każdego z podanych przedmiotów wskaż odpowiedni pojemnik na odpady lub sposób utylizacji:

        Plastik i metal (np. butelki plastikowe, pojemniki, puszki, folia aluminiowa, kartony po mleku)
        Papier (np. gazety, karton)
        Szkło (np. butelki szklane, słoiki)
        Odpady organiczne (np. resztki jedzenia, przedmioty kompostowalne)
        Odpady zmieszane – dla przedmiotów, które nie pasują do powyższych kategorii lub nie nadają się do recyklingu
        Odpady wielkogabarytowe – dla dużych przedmiotów (np. meble, sprzęty), które należy oddać do punktu zbiórki

    Dodatkowe informacje:
    Proszę podaj następujące szczegóły dotyczące wszystkich zidentyfikowanych przedmiotów:

        Z jakich materiałów są wykonane? Czy to szkło, plastik, metal, drewno, tkanina, itp.?
        Jakie mają rozmiary? Czy są małe, średnie, czy duże?
        Czy przedmioty są jednakowe, czy różnią się między sobą? Czy występuje różnorodność kolorów, kształtów i rozmiarów?
        Czy na obrazie widoczne są inne materiały, które mogą być przydatne? Np. włóczka, tkanina, papier, drewno?

    Dla każdego przedmiotu podaj kategorię w języku polskim, bez zbędnych symboli czy znaków specjalnych. Jeśli przedmiot pasuje do kilku kategorii, wybierz najwłaściwszą zgodnie z typowymi praktykami recyklingowymi. W przypadku przedmiotów trudnych do zakwalifikowania oznacz je jako "Nieokreślone" z krótkim uzasadnieniem.

    Odpowiedź zwracaj w formacie JSON takim jak poniżej:
        [
            {
                "item": "plastikowa butelka",
                "bin": "Plastik i metal",
                "explanation": "Wrzuć do pojemnika na plastik i metal.",
                "details": {
                    "material": "plastik",
                    "size": "duża",
                    "variety": "różne kolory"
                }
            },
            {
                "item": "kartonowe pudełko",
                "bin": "Papier",
                "explanation": "Wrzuć do pojemnika na papier.",
                "details": {
                    "material": "papier",
                    "size": "średnie",
                    "variety": "jednakowe"
                }
            },
            {
            "item": "Niezidentyfikowany przedmiot",
            "bin": "brak",
            "explanation": "Przedmiot jest zbyt niewyraźny, aby określić materiał i przeznaczenie.",
            "details": {
                "material": "Nieokreślony",
                "size": "Nieokreślony",
                "variety": "Nieokreślony"
            }
        }
        ]
        Otrzymasz zdjęcie w formacie webp
"""
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash") -> None:
        super().__init__(api_key, model, self.PROMPT)

    @log_execution
    async def generate_response(self, user_input) -> Optional[str]:
        if self.api_client and self.api_client.model_instance:
            response = await self.api_client.model_instance.generate_content_async([{"text":"."},
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
