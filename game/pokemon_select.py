from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect
from pokemon.base.player import PokemonStatus

if TYPE_CHECKING:
    from .combat import CombatScreen

arrow_right = pg.image.load("./assets/arrow_pixel_art_right.png").convert_alpha()


class PokemonSelectScreen():
    def __init__(self, screen: Surface, combat_screen: CombatScreen):
        self._screen = screen
        self._combat_screen = combat_screen
        self._pokemon_status = self._combat_screen.game_loop.player.get_pokemon_status()
        self._details_font = self._combat_screen.game_loop.display_info.details_font
        self._arrow_position = 0
        self._max_arrow_position = len(self._pokemon_status.pokemon) - 1

    # TODO: think about if I want to leave it this way with having the index disjointed with the PokemonStatus
    def create_pokemon_rect(self, index_id: int, pokemon: PokemonStatus, parent_rect: Optional[Rect]) -> Rect:
        hp = self._details_font.render(f"{pokemon.current_hp} / {pokemon.max_hp}", False, (0, 0, 0))
        name = self._details_font.render(f"{pokemon.name}", False, (0, 0, 0))
        level = self._details_font.render(f":L{pokemon.level}", False, (0, 0, 0))
        name_rect: Rect
        if parent_rect is not None:
            name_rect = name.get_rect(midtop=parent_rect.midbottom)
        else:
            name_rect = name.get_rect(centerx=self._screen.get_width()/2, top=0)
        hp_rect = hp.get_rect(midleft=name_rect.midright)
        level_rect = level.get_rect(midtop=name_rect.midbottom)

        self._screen.blit(hp, hp_rect)
        self._screen.blit(name, name_rect)
        self._screen.blit(level, level_rect)
        return level_rect

    def generate_pokemon_info(self):
        rect_list: List[Rect] = []
        for p_index in range(0, len(self._pokemon_status.pokemon)):
            parent_rect: Optional[Rect] = None
            if len(rect_list) != 0:
                parent_rect = rect_list[p_index-1]
            rect_list.append(self.create_pokemon_rect(p_index, self._pokemon_status.pokemon[p_index], parent_rect))

        self.render_arrow(rect_list)

    def render_arrow(self, rect_list: List[Rect]):
        rect = rect_list[self._arrow_position]
        a_rect = arrow_right.get_rect(midright=rect.midleft)
        self._screen.blit(arrow_right, a_rect)

    def render(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._combat_screen.game_loop.StopRunning()
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_UP, pg.K_w):
                    if self._arrow_position <= 0:
                        self._arrow_position = 0
                    else:
                        self._arrow_position -= 1
                if event.key in (pg.K_DOWN, pg.K_s):
                    if self._arrow_position >= self._max_arrow_position:
                        self._arrow_position = self._max_arrow_position
                    else:
                        self._arrow_position += 1
                if event.key in (pg.K_RETURN, pg.K_SPACE):
                    # selecting the selected pokemon
                    self._combat_screen.add_selected_player_pokemon(self._arrow_position)
                    self._combat_screen._selector_screen = None

                    pass
                if event.key == pg.K_ESCAPE:
                    self._combat_screen.game_loop.StopRunning()

        self.generate_pokemon_info()
