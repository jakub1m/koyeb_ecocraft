from .base_prompt_class import BasePrompt

class RecyclingGuide(BasePrompt):
    PROMPT = """Dla każdego z podanych przedmiotów wskaż odpowiedni pojemnik na odpady lub sposób utylizacji:

        Plastik i metal (np. butelki plastikowe, pojemniki, puszki, folia aluminiowa)
        Papier (np. gazety, karton)
        Szkło (np. butelki szklane, słoiki)
        Odpady organiczne (np. resztki jedzenia, przedmioty kompostowalne)
        Odpady zmieszane – dla przedmiotów, które nie pasują do powyższych kategorii lub nie nadają się do recyklingu
        Odpady wielkogabarytowe – dla dużych przedmiotów (np. meble, sprzęty), które należy oddać do punktu zbiórki

    Dla każdego przedmiotu podaj kategorię w języku polskim, bez zbędnych symboli czy znaków specjalnych. Jeśli przedmiot pasuje do kilku kategorii, wybierz najwłaściwszą zgodnie z typowymi praktykami recyklingowymi. W przypadku przedmiotów trudnych do zakwalifikowania oznacz je jako "Nieokreślone" z krótkim uzasadnieniem.

    Odpowiedź zwracaj w formacie JSON takim jak poniżej: [{'item': 'gaśnica', 'bin': 'Nieokreślone', 'explanation': 'Oddaj do punktu zbiórki odpadów niebezpiecznych.'}, {'item': 'worek', 'bin': 'Nieokreślone', 'explanation': 'W zależności od materiału: plastikowy - do plastiku i metalu, papierowy - do papieru, materiałowy - do odpadów zmieszanych.'}, {'item': 'puszka', 'bin': 'Metal', 'explanation': 'Wrzuć do pojemnika na plastik i metal.'}, {'item': 'puszka', 'bin': 'Metal', 'explanation': 'Wrzuć do pojemnika na plastik i metal.'}, {'item': 'butelka', 'bin': 'Nieokreślone', 'explanation': 'W zależności od materiału: szklana - do szkła, plastikowa - do plastiku i metalu.'}, {'item': 'słoik', 'bin': 'Szkło', 'explanation': 'Wrzuć do pojemnika na szkło.'}]
"""
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash") -> None:
        super().__init__(api_key, model, self.PROMPT)
