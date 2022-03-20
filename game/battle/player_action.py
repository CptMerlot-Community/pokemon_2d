from __future__ import annotations
from typing import TYPE_CHECKING, List
from pygame.surface import Surface
from pygame.rect import Rect
import pygame as pg
from enum import Enum

if TYPE_CHECKING:
    from game.combat import CombatScreen


class PlayerActionType(Enum):
    attack = 0
    pkmn = 1
    item = 2
    run = 3

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
                                        (int(self._screen.get_width() * .40),
                                            int(self._screen.get_height() -
                                                (self._screen.get_height() *
                                                 self._combat_screen.game_loop.display_info.combat_window_height)),
                                            int(self._screen.get_width() * .59),
                                            int(self._screen.get_height() *
                                                self._combat_screen.game_loop.display_info.combat_window_height)
                                         )
                                        )
        action_box = pg.transform.scale(self._box_surface,
                                        (action_scrn_rect.width,
                                         action_scrn_rect.height,
                                         )
                                        )

        self._screen.blit(action_box, action_scrn_rect)
        return action_scrn_rect

    def _generate_fight_rect(self, action_box_rect: Rect) -> Rect:
        fight_txt = self._combat_screen.game_loop.display_info.details_font.render(
            "FIGHT", False, self._combat_screen.game_loop.display_info.color_black_rbg)

        fight_txt_rect = fight_txt.get_rect(top=action_box_rect.top + action_box_rect.height * .3,
                                            left=action_box_rect.left + action_box_rect.width * .1)
        self._screen.blit(fight_txt, fight_txt_rect)
        return fight_txt_rect

    def _generate_pkmn_rect(self, fight_rect: Rect) -> Rect:
        pkmn_txt = self._combat_screen.game_loop.display_info.details_font.render(
            "PkMn", False, self._combat_screen.game_loop.display_info.color_black_rbg)

        pkmn_txt_rect = pkmn_txt.get_rect(top=fight_rect.top, left=fight_rect.left + 200)
        self._screen.blit(pkmn_txt, pkmn_txt_rect)
        return pkmn_txt_rect

    def _generate_item_rect(self, fight_rect: Rect) -> Rect:
        item_txt = self._combat_screen.game_loop.display_info.details_font.render(
            "ITEM", False, self._combat_screen.game_loop.display_info.color_black_rbg)

        item_txt_rect = item_txt.get_rect(top=fight_rect.top + 80, left=fight_rect.left)
        self._screen.blit(item_txt, item_txt_rect)
        return item_txt_rect

    def _generate_run_rect(self, pkmn_rect: Rect) -> Rect:
        run_txt = self._combat_screen.game_loop.display_info.details_font.render(
            "RUN", False, self._combat_screen.game_loop.display_info.color_black_rbg)

        run_txt_rect = run_txt.get_rect(top=pkmn_rect.top + 80, left=pkmn_rect.left)
        self._screen.blit(run_txt, run_txt_rect)
        return run_txt_rect

    def _render_action_box(self):
        action_box_rect = self._generate_action_box()
        fight_rect = self._generate_fight_rect(action_box_rect)
        pkmn_rect = self._generate_pkmn_rect(fight_rect)
        item_rect = self._generate_item_rect(fight_rect)
        run_rect = self._generate_run_rect(pkmn_rect)

        _action_map: List[List[Rect]] = [[fight_rect, pkmn_rect], [item_rect, run_rect]]
        self._render_arrow(_action_map)

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
                    if self._arrow_position_x == 0 and self._arrow_position_y == 0:
                        self._combat_screen.player_seclect_action(action_type=PlayerActionType.attack)
                    elif self._arrow_position_x == 1 and self._arrow_position_y == 0:
                        self._combat_screen.player_seclect_action(action_type=PlayerActionType.pkmn)
                    elif self._arrow_position_x == 0 and self._arrow_position_y == 1:
                        self._combat_screen.player_seclect_action(action_type=PlayerActionType.item)
                    else:  # if its none of the above its 1,1 which is the run action
                        self._combat_screen.player_seclect_action(action_type=PlayerActionType.run)

                if event.key == pg.K_ESCAPE:
                    self._combat_screen.game_loop.StopRunning()

        self._render_action_box()
