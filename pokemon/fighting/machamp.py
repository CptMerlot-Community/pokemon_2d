from .base import Fighting


class Machamp(Fighting):
    def __init__(self, **kwargs):
        self._evolves_to = None
        self._evolve_level = None
        self._hp_mod: float = .22
        self._sp_mod: float = .20
        self._def_mod: float = .24
        self._attk_mod: float = .29
        super().__init__(name="machamp", **kwargs)
