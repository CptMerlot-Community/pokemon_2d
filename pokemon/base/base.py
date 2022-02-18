from typing import Optional
import uuid

from pokemon.pokemons import pokemon


class Pokemon():
    _hp_mod: float = 0.0
    _sp_mod: float = 0.0
    _def_mod: float = 0.0
    _attk_mod: float = 0.0

    def __init__(self, name: str, level: int = 1):
        self.name = name
        self._id = uuid.uuid1()
        self._type: Optional[str] = None
        self._level = 10
        self._hitpoints: int = 0
        self._evolves_to: Optional[str] = None
        self._evolve_level: Optional[int] = None
        self._roll_stats()

    def _roll_stats(self):
        self._hitpoints = int((10 * self._level) + ((10 * self._level) * self._hp_mod))

    def _lookup_pokemon_data(self):
        if self._type.lower() in pokemon.keys():
            if self.name.lower() in pokemon[self._type.lower()]:
                self._evolves_to = pokemon[self._type.lower()][self.name.lower()]["evolves_to"]
                self._evolve_level = pokemon[self._type.lower()][self.name.lower()]["evolution_level"]

    def evolves_to(self) -> str:
        if self._evolves_to is not None:
            return "{} at level {}".format(self._evolves_to, self._evolve_level)
        return "n/a"

    def level_up(self):
        self._level = self._level + 1

    def __str__(self) -> str:
        return("name: {1} type: {2} level: {3} id: {0}".format(self._id, self.name, self._type, self._level))
