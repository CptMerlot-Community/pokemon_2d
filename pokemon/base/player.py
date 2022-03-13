from dataclasses import dataclass
from typing import List, Any, Optional
from .pokemon import Pokemon
from uuid import uuid4
from dataclasses import dataclass


@dataclass
class PokemonStatus:
    def __init__(self, pokemon: Pokemon):
        self.level = pokemon.level
        self.max_hp = pokemon.hitpoints
        self.current_hp = pokemon.current_hitpoints
        self.name = pokemon.name
        self.alive = pokemon.alive


@dataclass
class PlayerPokemonStatus:
    def __init__(self, pokemons: List[Pokemon]):
        self._pokemon: List[PokemonStatus] = []
        for pokemon in pokemons:
            self._pokemon.append(PokemonStatus(pokemon))


class Player():
    _pokemons: List[Pokemon] = []
    # _items: List[Any] = []
    _name: str = ""
    _active_pokemon: Optional[Pokemon] = None

    def __init__(self, name: str = ""):
        self._uuid = uuid4()
        self._name = name

    @property
    def pokemons(self) -> List[Pokemon]:
        return self._pokemons

    @property
    def active_pokemon(self) -> Optional[Pokemon]:
        return self._active_pokemon

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if self._name == "":
            self._name = name

    def pokemon_count(self) -> int:
        return len(self.pokemons)

    # TODO: Handle edge cases of location_id not having pokemons for the below methods
    def get_pokemon(self, location_id: int) -> Pokemon:
        self._active_pokemon = self._pokemons[location_id]
        return self._active_pokemon

    def add_pokemon(self, pokemon: Pokemon):
        if self.pokemon_count() == 0:
            self._active_pokemon = pokemon
        if self.pokemon_count() < 6:
            self._pokemons.append(pokemon)

    def remove_pokemon(self, location_id: int):
        if self._pokemons[location_id] != self._active_pokemon:
            # TODO: this will discard a pokemon
            self._pokemons.pop(location_id)

    def get_pokemon_status(self) -> PlayerPokemonStatus:
        """Return a list of information regarding current pokemon and their status
        """
        return PlayerPokemonStatus(self.pokemons)

    def check_if_available_pokemons(self) -> bool:
        for pokemon in self.pokemons:
            if pokemon.alive:
                return True
        return False
