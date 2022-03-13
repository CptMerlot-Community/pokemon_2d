from __future__ import annotations
from typing import TYPE_CHECKING
import pygame as pg
from pygame.surface import Surface


if TYPE_CHECKING:
    from .combat import CombatScreen

arrow_right = pg.image.load("./assets/arrow_pixel_art_right.jpg").convert_alpha()


class PokemonSelectScreen():
    def __init__(self, screen: Surface, combat_screen: CombatScreen):
        self._screen = screen
        self._combat_screen = combat_screen
        self._pokemon_list = self._combat_screen.game_loop.player.get_pokemon_status()

    def render(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._game_loop.StopRunning()
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_UP, pg.K_w):
                    # move the arrow up pokemon list
                    pass
                if event.key in (pg.K_DOWN, pg.K_s):
                    # move the arrow down the pokemon list
                    pass
                if event.key == pg.K_ESCAPE:
                    self._game_loop.StopRunning()

        self._screen.fill((0, 0, 0))
        wf = self._game_loop.display_info.welcome_font.render("Welcome to Pokemon 2d", False, (255, 255, 255))
        wf_rect = wf.get_rect(center=(self._screen.get_width() / 2, self._screen.get_height() / 2))
        self._screen.blit(wf, wf_rect)
