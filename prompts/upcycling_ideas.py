from .base_prompt_class import BasePrompt

class UpcyclingIdeas(BasePrompt):
    PROMPT = """
    Na podstawie dostarczonej listy przedmiotów wygeneruj kreatywną listę projektów upcyklingowych, które łączą wiele różnych materiałów w unikalny i wartościowy sposób. Twoim celem jest zaproponowanie innowacyjnych pomysłów, które przekształcą podane przedmioty w nowe, funkcjonalne lub dekoracyjne obiekty.

Dla każdego projektu:
1. **Krótki opis projektu upcyklingowego** – opisz, jak połączyć podane przedmioty w konkretny projekt.
2. **Dodatkowe elementy** – jeśli konieczne będzie dokupienie dodatkowych materiałów (np. deska, farby, śruby), wspomnij o tym i podkreśl, jak wpłynie to na końcowy efekt. Napisz o tym w sekcji "description".

Format odpowiedzi:
[    {        "project": "Stół z palet i szyby",         "description": "Wykorzystaj drewniane palety jako bazę stołu i dokup szybę, by stworzyć elegancki i funkcjonalny mebel. Palety można oszlifować i pomalować, by nadać im bardziej nowoczesny lub rustykalny charakter. Szyba pełni funkcję blatu, co sprawia, że całość jest trwała i łatwa w utrzymaniu czystości. To idealne rozwiązanie dla jadalni lub przestrzeni ogrodowej."    },    {        "project": "Fotel z opon i pianki tapicerskiej",         "description": "Przekształć starą oponę w wygodny fotel, dokładając okrągłą deskę na spód (stabilizacja) oraz warstwę pianki tapicerskiej i materiału obiciowego na górę. Do opony można dokupić nóżki meblowe lub zamontować je na ramie drewnianej. Tak stworzony mebel łączy trwałość opony z nowoczesnym designem, idealnym do wnętrz lub na taras."    }]

    """
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash") -> None:
        super().__init__(api_key, model, self.PROMPT)
