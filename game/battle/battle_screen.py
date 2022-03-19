from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple
import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect
from pokemon.base.pokemon import Pokemon
from pokemon.combat.fight import Combat
from game.render.fonts import word_wrap  # type: ignore
from game.battle.pokemon_select import PokemonSelectScreen
from game.battle.player_action import PlayerAction


if TYPE_CHECKING:
    from game.combat import CombatScreen


box1 = pg.image.load("./assets/BOX_1.png").convert_alpha()
box2 = pg.image.load("./assets/BOX_2.png").convert_alpha()

pLine = pg.image.load("./assets/line_1_new.png").convert_alpha()
eLine = pg.image.load("./assets/line_2_new.png").convert_alpha()

arrow_right = pg.image.load("./assets/arrow_pixel_art_right.png").convert_alpha()

p_pokemon = pg.image.load("./assets/Character_11_seafoam.png").convert_alpha()
e_pokemon = pg.image.load("./assets/Character_9_baby_pink.png").convert_alpha()


class BattleScreen():

    def __init__(self, combat_screen: CombatScreen, combat: Combat):
        self._combat_screen = combat_screen
        self._combat: Combat = combat
        self._screen = self._combat_screen._screen
        self.game_loop = self._combat_screen.game_loop
        self._combat_screen.set_combat_text(f"A wild {combat._computer_pokemon.name} has appeared.")

    def _draw_details(self,
                      pokemon_sprite: Surface,
                      line_sprite: Surface,
                      pokemon_rect: Rect,
                      detail_rect: Rect,
                      pokemon: Pokemon,
                      skip_hp=False):
        poke = pg.transform.scale(pokemon_sprite, (pokemon_rect.width, pokemon_rect.height))
        self._screen.blit(poke, pokemon_rect.topleft)

        hp_rect = self._draw_hp_detail(pokemon, detail_rect, skip_hp)
        hp_bar_rect = self._draw_hp_bar_detail(pokemon, hp_rect)
        hp_level_rect = self._draw_level_detail(pokemon.level, hp_bar_rect)
        _ = self._draw_name_detail(pokemon.name, hp_level_rect)

        p_line = pg.transform.scale(line_sprite, (detail_rect.width, detail_rect.height))
        self._screen.blit(p_line, detail_rect.topleft)

    def _draw_level_detail(self, pokemon_level: int, hp_bar_rect: Rect) -> Rect:
        level = self.game_loop.display_info.details_font.render(f"L:{pokemon_level}", False, (0, 0, 0))
        level_rect = level.get_rect(midbottom=hp_bar_rect.midtop)
        self._screen.blit(level, level_rect)
        return level_rect

    def _draw_name_detail(self, pokemon_name: str, level_rect: Rect) -> Rect:
        name = self.game_loop.display_info.details_font.render(f"{pokemon_name}", False, (0, 0, 0))
        name_rect = name.get_rect(midbottom=level_rect.midtop)
        self._screen.blit(name, name_rect)
        return name_rect

    def _draw_hp_bar_detail(self, pokemon: Pokemon, hp_rect: Rect) -> Rect:
        hp_precent = (pokemon.current_hitpoints / pokemon.hitpoints)
        hp_bar_rect = pg.draw.rect(self._screen, (0, 0, 0), (hp_rect.left,
                                   hp_rect.top-hp_rect.height,
                                   self.game_loop.display_info.hp_bar_width,
                                   int(hp_rect.height * .50)), 1)
        hp_precent_color = (7, 117, 1)
        if hp_precent < 0.30:
            hp_precent_color = (255, 76, 5)
        elif hp_precent <= 0.50:
            hp_precent_color = (167, 176, 2)
        pg.draw.rect(self._screen, hp_precent_color, (*hp_bar_rect.topleft,
                                                      self.game_loop.display_info.hp_bar_width * hp_precent,
                                                      int(hp_rect.height * .50)), 0)

        hp_string = self.game_loop.display_info.details_font.render("HP:", False, (0, 0, 0))
        hp_string_rect = hp_string.get_rect(midright=hp_bar_rect.midleft)
        self._screen.blit(hp_string, hp_string_rect)
        return hp_bar_rect

    def _draw_hp_detail(self, pokemon: Pokemon, detail_rect: Rect, skip_hp: bool) -> Rect:
        hp = self.game_loop.display_info.details_font.render("{0} / {1}".format(
                                                             pokemon.current_hitpoints,
                                                             pokemon.hitpoints),
                                                             False, (0, 0, 0))
        hp_rect = hp.get_rect(left=(detail_rect.left +
                                    (detail_rect.width * self.game_loop.display_info.detail_text_start_left_mod)),
                              bottom=detail_rect.bottom -

                              (detail_rect.height * self.game_loop.display_info.detail_text_start_bottom_mod))
        if not skip_hp:
            self._screen.blit(hp, hp_rect)
        return hp_rect

    def _draw_enemy_details(self, player_pokemon_rect: Rect, player_detail_rect: Rect):
        pokemon_rect = pg.rect.Rect(self._screen.get_width() - int(self._screen.get_width()/2.7),
                                    (player_detail_rect.top - self.game_loop.display_info.pokemon_size[1]) * .50,
                                    *self.game_loop.display_info.pokemon_size)
        detail = pg.rect.Rect(0 + (self._screen.get_width()/50),
                              (player_pokemon_rect.top - self.game_loop.display_info.detail_size[1])*.50,
                              *self.game_loop.display_info.detail_size)
        if self._combat is not None:
            self._draw_details(e_pokemon, eLine, pokemon_rect, detail, self._combat._computer_pokemon, True)

    def _draw_player_details(self, combat_txt_screen: Rect) -> Tuple[Rect, Rect]:
        # TODO: move dynamic sizing into the display_info class

        pokemon_rect = pg.rect.Rect(combat_txt_screen.left + int(combat_txt_screen.width / 10),
                                    ((self._screen.get_height() - combat_txt_screen.height) -
                                    self.game_loop.display_info.pokemon_size[1]),
                                    *self.game_loop.display_info.pokemon_size)
        detail_rect = pg.rect.Rect((self._screen.get_width() -
                                    self._screen.get_width()/2.5) -
                                   self._screen.get_width()/50,
                                   (self._screen.get_height() - combat_txt_screen.height) -
                                   self.game_loop.display_info.detail_size[1],
                                   *self.game_loop.display_info.detail_size)
        if self._combat is None:
            raise BaseException("Combat has not started?")
        self._draw_details(p_pokemon, pLine, pokemon_rect, detail_rect, self._combat._player_pokemon)
        return pokemon_rect, detail_rect

    def _draw_combat_details(self, combat_txt_screen: Rect):
        # TODO: Have player details be created so enemy details
        # can be drawn in relation to the player rects
        pokemon_rect, detail_rect = self._draw_player_details(combat_txt_screen)
        self._draw_enemy_details(pokemon_rect, detail_rect)

    def render(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_loop.StopRunning()
            if self._combat_screen._fainted_pokemon is not None:
                if event.type == pg.KEYDOWN:
                    if event.key in (pg.K_RETURN, pg.K_SPACE, pg.K_ESCAPE):
                        if self._combat_screen._fainted_pokemon is self.game_loop.player.active_pokemon:
                            if not self.game_loop.player.check_if_available_pokemons():
                                self.game_loop.GameOver(True)
                            else:
                                self._combat_screen.pokemon_select_screen()
                        else:
                            self.game_loop.ExitCombat()
            else:
                if event.type == pg.KEYDOWN:
                    if event.key in (pg.K_RETURN, pg.K_SPACE):
                        attk_pokemon = self._combat.attack_pokemon.name
                        def_pokemon = self._combat.defending_pokemon.name
                        self._combat_text = f"{attk_pokemon} hits {def_pokemon} for {self._combat.attack()}"
                        self._combat_screen._fainted_pokemon = self._combat.pokemon_fainted()
                        if self._combat_screen._fainted_pokemon is not None:
                            self._combat_text = f"{self._combat_screen._fainted_pokemon.name} has fainted..."
                    if event.key == pg.K_ESCAPE:
                        self.game_loop.StopRunning()

        self._draw_combat_details(self._combat_screen._combat_text_screen_rect)
