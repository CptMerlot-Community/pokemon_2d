from .base import Fighting
from pokemon.attack.claw import Claw


class Machoke(Fighting):
    def __init__(self, **kwargs):
        self._evolves_to = "machamp"
        self._evolve_level = 45
        self._hp_mod: float = .20
        self._sp_mod: float = .18
        self._def_mod: float = .23
        self._attk_mod: float = .25
        self._attacks = [Claw]
        super().__init__(name="machoke", **kwargs)
