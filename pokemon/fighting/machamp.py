from .base import Fighting


class Machamp(Fighting):
    def __init__(self, **kwargs):
        super().__init__(name="machop", **kwargs)
        self._evolves_to = None
        self._evolve_level = None
        self._hp_mod: float = .22
        self._sp_mod: float = .16
        self._def_mod: float = .21
        self._attk_mod: float = .24
