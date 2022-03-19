from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple
import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect
from pokemon.base.pokemon import Pokemon
from pokemon.combat.fight import Combat


if TYPE_CHECKING:
    from game.combat import CombatScreen


class CombatStart():

    def __init__(self, combat_screen: CombatScreen):
        self._combat_screen = combat_screen
        self._screen = self._combat_screen._screen
        self.game_loop = self._combat_screen.game_loop

    def render(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_loop.StopRunning()
            else:
                if event.type == pg.KEYDOWN:
                    if event.key in (pg.K_RETURN, pg.K_SPACE):
                        self._combat_screen.combat_open_over()
                    if event.key == pg.K_ESCAPE:
                        self.game_loop.StopRunning()
