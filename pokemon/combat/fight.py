from typing import Optional
from pokemon.base.pokemon import Pokemon
import random
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

    def send_in_new_player_pokemon(self, pokemon: Optional[Pokemon]):
        if pokemon is not None:
            if self._current_turn == self._player_pokemon:
                self._player_pokemon = pokemon
                self._current_turn = self._player_pokemon
            else:
                self._player_pokemon = pokemon

    @property
    def attack_pokemon(self):
        return self._current_turn

    @property
    def defending_pokemon(self):
        if self._current_turn._id == self._player_pokemon._id:
            return self._computer_pokemon
        return self._player_pokemon

    def _first_action(self) -> Pokemon:
        if self._player_pokemon.speed == self._computer_pokemon.speed:
            if random.randint(0, 1) == 0:
                return self._player_pokemon
        if self._player_pokemon.speed > self._computer_pokemon.speed:
            return self._player_pokemon
        return self._computer_pokemon

    def is_combat_over(self) -> bool:
        return self._is_defending_pokemon_dead()

    def _is_defending_pokemon_dead(self) -> bool:
        return not self.defending_pokemon.alive

    def pokemon_fainted(self) -> Optional[Pokemon]:
        if not self.defending_pokemon.alive:
            return self.defending_pokemon
        if not self.attack_pokemon.alive:
            return self.attack_pokemon
        return None

    def attack(self) -> int:
        dmg = self._roll_attack()
        self.defending_pokemon.take_damage(dmg)
        self._current_turn = self.defending_pokemon
        return dmg

    # TODO: Make roll attack take in the AP and Defense to reduce logic from roll attack and roll special
    def _roll_attack(self) -> int:
        mod = operator.truediv(self.attack_pokemon.attack_power, self.defending_pokemon.defense)
        if mod > 1:
            mod = 1
        dmg = int((self.attack_pokemon.attack_power * mod) * self._dmg_type_mod())
        # TODO: Add logic if the overkill isn't by a certain amount the pokemon lives
        # with 1hp until next round. We can flag this as a pokemon 1shot protection or something
        return dmg

    def _roll_special_attack(self) -> int:
        mod = operator.truediv(self.attack_pokemon.special_attack_power, self.defending_pokemon.special_defense)
        if mod > 1:
            mod = 1
        dmg = int((self.attack_pokemon.attack_power * mod) * self._dmg_type_mod())
        # TODO: Add logic if the overkill isn't by a certain amount the pokemon lives
        # with 1hp until next round. We can flag this as a pokemon 1shot protection or something
        return dmg

    def _dmg_type_mod(self) -> float:
        if any(t in self.attack_pokemon.type for t in self.defending_pokemon.vulnerable):
            return 1.45
        elif any(t in self.attack_pokemon.type for t in self.defending_pokemon.weak):
            return 1.20
        elif any(t in self.attack_pokemon.type for t in self.defending_pokemon.strong):
            return 0.80
        elif any(t in self.attack_pokemon.type for t in self.defending_pokemon.resistant):
            return 0.50
        else:
            return 1.0
