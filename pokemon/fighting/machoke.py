from .base import Fighting


class Machoke(Fighting):
    def __init__(self, **kwargs):
        self._hp_mod: float = .18
        self._sp_mod: float = .16
        self._def_mod: float = .21
        self._attk_mod: float = .24
        super().__init__(name="machop", **kwargs)
        self._evolves_to = "machamp"
        self._evolve_level = 45
