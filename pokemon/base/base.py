from typing import Optional, Tuple, Dict, List
import uuid
import random
from pokemon.attack.base import Attack


class Pokemon():
    _type: Optional[str] = None
    _evolves_to: Optional[str] = None
    _evolve_level: Optional[int] = None
    _base_stat_value = 10
    _hp_mod: float = 0.0
    _sp_mod: float = 0.0
    _def_mod: float = 0.0
    _attk_mod: float = 0.0
    _level = 0
    _hitpoints: int = 0
    _attk_pw: int = 0
    _defense: int = 0
    _speed: int = 0
    _experience: int = 0
    _current_hitpoints: int = 0
    _attacks: List[Attack] = []

    def __init__(self, name: str, level_range: Tuple[int, int]) -> None:
        self.name = name
        self._id = uuid.uuid1()
        self._roll_for_level(level_range)
        self._roll_stats()

    def _roll_for_level(self, level_range: Tuple[int, int]) -> None:
        min, max = level_range
        self._level = random.randint(min, max)

    def _roll_stats(self) -> None:
        self._hitpoints = self._roll_stat(self._hp_mod)
        self._attk_pw = self._roll_stat(self._attk_mod)
        self._speed = self._roll_stat(self._sp_mod)
        self._defense = self._roll_stat(self._def_mod)

    def _roll_stat(self, mod: float) -> int:
        return int((self._base_stat_value * self._level) + ((self._base_stat_value * self._level) * mod))

    def evolves_to(self) -> str:
        if self._evolves_to is not None:
            return "{} at level {}".format(self._evolves_to, self._evolve_level)
        return "n/a"

    def level_up(self) -> None:
        self._level = self._level + 1
        if self._evolve_level is not None:
            if self._level >= self._evolve_level:
                answer = input(f"would you like to evolve {self.name} to {self.evolves_to}")
                if answer.lower() == "yes":
                    self._evolve()

    def _evolve(self) -> None:
        # evolve pokemon here
        # update base mod values
        # name and evolve to and evolve level
        # reroll stats
        self._roll_stats()
        pass

    def _combat_experience(self) -> None:
        # roll for exp
        # self._experience + get_exp()
        pass

    def take_damage(self, dmg: int) -> bool:
        self._mins_hp(dmg)
        return self._check_if_dead()

    def _check_if_dead(self) -> bool:
        return self._current_hitpoints is 0

    def _mins_hp(self, dmg: int) -> None:
        if self._current_hitpoints < dmg:
            self._current_hitpoints = 0
            return

        self._current_hitpoints = self._current_hitpoints - dmg
        return

    def get_stats(self) -> Dict[str, int]:
        return {
            "attack": self._attk_pw,
            "defense": self._defense,
            "speed": self._speed,
            "hitpoints": self._hitpoints,
            "level": self._level,
            "experience": self._experience,
        }

    def __str__(self) -> str:
        return("name: {1} type: {2} level: {3} id: {0}".format(self._id, self.name, self._type, self._level))
