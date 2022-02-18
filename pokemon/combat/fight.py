from pokemon.base.base import Pokemon


class Combat():
    def __init__(self, player_pokemon: Pokemon, computer_pokemon: Pokemon):
        self._player_pokemon = player_pokemon
        self._computer_pokemon = computer_pokemon

    # def
