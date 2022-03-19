from __future__ import annotations
from typing import TYPE_CHECKING, List
from pygame.surface import Surface
from pygame.rect import Rect
import pygame as pg

if TYPE_CHECKING:
    from game.combat import CombatScreen

# x,y = 0,0 Fight - 0,1 PkMn - 1,0 Item - 1,1 RUN
# (int, int) = x+1 x-1 x can not be greater than 1 or less than 0
# (int, int) = y+x y-1 y can not be greater than 1 or less than 0


class PlayerAction:
    def __init__(self, combat_screen: CombatScreen, box_surface: Surface, arrow_surface: Surface):
        self._combat_screen = combat_screen
        self._screen = self._combat_screen._screen
        self._box_surface = box_surface
        self._arrow_surface = arrow_surface
        self._arrow_position_x = 0
        self._arrow_position_y = 0

    def _generate_action_box(self) -> Rect:

        action_scrn_rect = pg.draw.rect(self._screen,
                                        (self._combat_screen.game_loop.display_info.color_off_white_rbg),
                                        (self._screen.get_width() * .65,
                                            int(self._screen.get_height() -
                                                (self._screen.get_height() *
                                                 self._combat_screen.game_loop.display_info.combat_window_height)),
                                            self._screen.get_width() * .34,
                                            int(self._screen.get_height() *
                                                self._combat_screen.game_loop.display_info.combat_window_height)
                                         )
                                        )
        action_box = pg.transform.scale(self._box_surface,
                                        (action_scrn_rect.width,
                                         action_scrn_rect.height,
                                         )
                                        )
        action_box_rect = Rect(action_scrn_rect.left + int(action_box.get_width() / 3),
                               action_scrn_rect.top + int(action_box.get_height() / 4),
                               action_box.get_width() - int(action_scrn_rect.width / 20),
                               action_box.get_height() - int(action_scrn_rect.height / 5))

        self._screen.blit(action_box, action_scrn_rect)
        return action_box_rect

    def _render_action_box(self):
        action_box_rect = self._generate_action_box()

        _action_map: List[List[Rect]] = []
        # self._render_arrow(_action_map)

    # [[y_0x0_rect, y_0x1_rect], [y_1x0_rect, y1_x1_rect]]
    def _render_arrow(self, action_map: List[List[Rect]]):
        rect = action_map[self._arrow_position_y][self._arrow_position_x]
        arrow_rect = Rect(
            rect.left-self._combat_screen.game_loop.display_info.select_pokemon_arrow[0],
            rect.top, *self._combat_screen.game_loop.display_info.select_pokemon_arrow)
        arrow = pg.transform.scale(self._arrow_surface, (arrow_rect.width, arrow_rect.height))
        self._screen.blit(arrow, arrow_rect.topleft)

    def render(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._combat_screen.game_loop.StopRunning()
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_UP, pg.K_w):
                    if self._arrow_position_y <= 0:
                        self._arrow_position_y = 0
                    else:
                        self._arrow_position_y -= 1
                if event.key in (pg.K_DOWN, pg.K_s):
                    if self._arrow_position_y >= 1:
                        self._arrow_position_y = 1
                    else:
                        self._arrow_position_y += 1
                if event.key in (pg.K_LEFT, pg.K_a):
                    if self._arrow_position_x <= 0:
                        self._arrow_position_x = 0
                    else:
                        self._arrow_position_x -= 1
                if event.key in (pg.K_RIGHT, pg.K_d):
                    if self._arrow_position_x >= 1:
                        self._arrow_position_x = 1
                    else:
                        self._arrow_position_x += 1
                if event.key in (pg.K_RETURN, pg.K_SPACE):
                    self._combat_screen.set_player_turn(False)
                    # self._combat_screen.pokemon_select_screen()
                if event.key == pg.K_ESCAPE:
                    self._combat_screen.game_loop.StopRunning()

        self._render_action_box()
