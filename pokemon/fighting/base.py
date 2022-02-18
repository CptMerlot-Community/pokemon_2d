from ..base.base import Pokemon


class Fighting(Pokemon):
    _weak = ["Fairy", "Flying", "Psychic"]
    _effective = ["Dark", "Ice", "Normal", "Rock", "Steel"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._type = "Fighting"
