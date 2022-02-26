from pokemon.base.base import Pokemon
import operator


class Combat():
    def __init__(self, player_pokemon: Pokemon, computer_pokemon: Pokemon):
        """Starts combat between two given pokemon

        Args:
            player_pokemon (Pokemon): Players current active pokemon
            computer_pokemon (Pokemon): Computers current active pokemon
        """
        self._player_pokemon = player_pokemon
        self._computer_pokemon = computer_pokemon
        self._current_turn: Pokemon = self._first_action()

    def _first_action(self) -> Pokemon:
        if self._player_pokemon.speed > self._computer_pokemon.speed:
            return self._player_pokemon
        return self._computer_pokemon

    def is_combat_over(self) -> bool:
        return self._is_defending_pokemon_dead()

    def _is_defending_pokemon_dead(self) -> bool:
        return not self._defending_pokemon().alive

    def _defending_pokemon(self) -> Pokemon:
        if self._current_turn._id == self._player_pokemon._id:
            return self._computer_pokemon
        return self._player_pokemon

    def attack(self) -> bool:
        defending_pokemon = self._defending_pokemon()
        dmg = self._roll_attack(self._current_turn, defending_pokemon)
        defending_pokemon.take_damage(dmg)
        if self._is_defending_pokemon_dead():
            return True

        self._current_turn = defending_pokemon
        return False

    def _roll_attack(self, attack_pokemon: Pokemon, defending_pokemon: Pokemon) -> int:
        mod = operator.truediv(attack_pokemon.attack_power, defending_pokemon.defense)
        if mod > 1:
            mod = 1
        dmg = int(attack_pokemon.attack_power * mod)
        # TODO: Add logic if the overkill isn't by a certain amount the pokemon lives
        # with 1hp until next round. We can flag this as a pokemon 1shot protection or something
        return dmg
