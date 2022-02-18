from .base import Fighting
from pokemon.attack.claw import Claw


class Machop(Fighting):
    def __init__(self, **kwargs):
        self._evolves_to = "machoke"
        self._evolve_level = 23
        self._hp_mod: float = .18
        self._sp_mod: float = .16
        self._def_mod: float = .21
        self._attk_mod: float = .24
        self._attacks = [Claw]
        super().__init__(name="machop", **kwargs)
