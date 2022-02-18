from ..base.base import Pokemon


class Flying(Pokemon):
    _weak = ["Rock", "Steel", "Electric"]
    _effective = ["Fighting", "Bug", "Grass"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._type = "Flying"
        self._lookup_pokemon_data()
