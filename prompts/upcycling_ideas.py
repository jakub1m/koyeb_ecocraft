from .base_prompt_class import BasePrompt

class UpcyclingIdeas(BasePrompt):
    PROMPT = """
    Na podstawie dostarczonej listy przedmiotów wygeneruj listę pomysłów na projekty upcyklingowe, które w kreatywny sposób łączą wiele przedmiotów w jeden projekt. Dla każdego pomysłu dołącz
    Krótki opis projektu upcyklingowego.
    Skoncentruj się na innowacyjnych i praktycznych sugestiach, które przekształcają połączone materiały w nowe, funkcjonalne lub dekoracyjne przedmioty. Podkreśl zrównoważony rozwój i potencjał stworzenia czegoś wartościowego z materiałów odpadowych.
    Zwróć wynik w formacie:
    [
    {"project": "Lampy z butelek", "description": "„Zamień butelki w oryginalne klosze lamp. Wycinając je w różne kształty i rozmiary oraz malując na różne kolory, stworzysz unikalne ozdoby. Połącz te elementy z żarówką, by uzyskać nietypowe, kreatywne lampy, które będą wprowadzać do wnętrza niepowtarzalny klimat.”"}
    ]
    """
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash") -> None:
        super().__init__(api_key, model, self.PROMPT)
