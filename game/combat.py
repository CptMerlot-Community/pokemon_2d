from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect
from pokemon.base.base import Pokemon
from pokemon.pokemons import GeneratePokemon
from pokemon.combat.fight import Combat
from game.render.fonts import word_wrap  # type: ignore


if TYPE_CHECKING:
    from .loop import GameLoop

combat_window_height = .30

white = 255, 255, 255
off_white = 220, 220, 220

box1 = pg.image.load("./assets/BOX_1.png").convert_alpha()
box2 = pg.image.load("./assets/BOX_2.png").convert_alpha()

pLine = pg.image.load("./assets/line_1_new.png").convert_alpha()
eLine = pg.image.load("./assets/line_2_new.png").convert_alpha()

p_pokemon = pg.image.load("./assets/Character_11_seafoam.png").convert_alpha()
e_pokemon = pg.image.load("./assets/Character_9_baby_pink.png").convert_alpha()


class CombatScreen():
    _combat: Combat

    def __init__(self, screen: Surface, game_loop: GameLoop):
        self._screen = screen
        self._combat_text = ""
        self._game_loop = game_loop
        self.start_new_combat()
        self._winning_pokemon: Optional[Pokemon] = None

    def start_new_combat(self):
        p1 = GeneratePokemon(l_range=(4, 4), pokemons=[1, 4, 19, 43])
        c1 = GeneratePokemon(l_range=(4, 4), pokemons=[1, 4, 19, 43])
        self._combat = Combat(p1, c1)
        self._combat_text = f"A wild {c1.name} has appeared."
        self._winning_pokemon = None

    def _draw_details(self,
                      pokemon_sprite: Surface,
                      line_sprite: Surface,
                      pokemon_rect: Rect,
                      detail_rect: Rect,
                      pokemon: Pokemon):
        poke = pg.transform.scale(pokemon_sprite, (pokemon_rect.width, pokemon_rect.height))
        self._screen.blit(poke, pokemon_rect.topleft)

        hp = self._game_loop.display_info.details_font.render("{0} / {1}".format(
                                                             pokemon.current_hitpoints,
                                                             pokemon.hitpoints),
                                      False, (0, 0, 0))
        hp_rect = hp.get_rect(
                              centerx=detail_rect.centerx + (detail_rect.width * .10),
                              bottom=detail_rect.bottom - (detail_rect.height * .20))
        hp_bar = self._game_loop.display_info.details_font.render("------------", False, (0, 0, 0))
        hp_bar_rect = hp_bar.get_rect(midbottom=hp_rect.midtop)
        hp_string = self._game_loop.display_info.details_font.render("HP: ", False, (0, 0, 0))
        hp_string_rect = hp_string.get_rect(midright=hp_bar_rect.midleft)
        level = self._game_loop.display_info.details_font.render(f"L:{pokemon.level}", False, (0, 0, 0))
        level_rect = level.get_rect(midbottom=hp_bar_rect.midtop)
        name = self._game_loop.display_info.details_font.render(f"{pokemon.name}", False, (0, 0, 0))
        name_rect = name.get_rect(midbottom=level_rect.midtop)

        self._screen.blit(hp, hp_rect)
        self._screen.blit(hp_bar, hp_bar_rect)
        self._screen.blit(hp_string, hp_string_rect)
        self._screen.blit(name, name_rect)
        self._screen.blit(level, level_rect)

        p_line = pg.transform.scale(line_sprite, (detail_rect.width, detail_rect.height))
        self._screen.blit(p_line, detail_rect.topleft)

    def _draw_enemy_details(self):
        pokemon_height = self._screen.get_height() / 2.5
        detail_height = self._screen.get_height()/5.5
        pokemon_rect = pg.rect.Rect((self._screen.get_width() - int(self._screen.get_width()/2.7),
                                     self._screen.get_height()/20,
                                     self._screen.get_width()/3,
                                     pokemon_height))
        detail = pg.rect.Rect((0 + (self._screen.get_width()/50),
                               self._screen.get_height()/20,
                               self._screen.get_width()/2.5,
                               detail_height))
        self._draw_details(e_pokemon, eLine, pokemon_rect, detail, self._combat._computer_pokemon)

    def _draw_player_details(self, combat_screen: Rect):
        pokemon_height = self._screen.get_height() / 2.5
        detail_height = self._screen.get_height()/5.5
        pokemon_rect = pg.rect.Rect((combat_screen.left + int(combat_screen.width / 10),
                                     ((self._screen.get_height() - combat_screen.height) - pokemon_height),
                                     combat_screen.width / 3,
                                     pokemon_height))
        detail = pg.rect.Rect(((self._screen.get_width() - self._screen.get_width()/2.5) - self._screen.get_width()/50,
                               (self._screen.get_height() - combat_screen.height) - detail_height,
                               self._screen.get_width()/2.5,
                               detail_height))
        self._draw_details(p_pokemon, pLine, pokemon_rect, detail, self._combat._player_pokemon)

    def _draw_combat_details(self, combat_screen: Rect):
        # TODO: Have player details be created so enemy details
        # can be drawn in relation to the player rects
        self._draw_player_details(combat_screen)
        self._draw_enemy_details()

    def attack_screen(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._game_loop.StopRunning()
            if self._winning_pokemon is not None:
                if event.type == pg.KEYDOWN:
                    if event.key in (pg.K_RETURN, pg.K_SPACE, pg.K_ESCAPE):
                        self.start_new_combat()
            else:
                if event.type == pg.KEYDOWN:
                    if event.key in (pg.K_RETURN, pg.K_SPACE):
                        attk_pokemon = self._combat.attack_pokemon.name
                        def_pokemon = self._combat.defending_pokemon.name
                        dmg = self._combat.attack()
                        self._combat_text = f"{attk_pokemon} hits {def_pokemon} for {dmg}"
                        self._winning_pokemon = self._combat.winning_pokemon()
                        if self._winning_pokemon is not None:
                            self._combat_text = f"{self._winning_pokemon.name} has won"
                    if event.key == pg.K_ESCAPE:
                        self._game_loop.StopRunning()

        self._screen.fill(off_white)

        # combat screen
        c_scrn_rect = pg.draw.rect(self._screen,
                                   (off_white),
                                   (-10,
                                    int(self._screen.get_height()-(self._screen.get_height()*combat_window_height)),
                                    self._screen.get_width(),
                                    int(self._screen.get_height()*combat_window_height)
                                    )
                                   )

        self._draw_combat_details(c_scrn_rect)

        box_1 = pg.transform.scale(box1,
                                   (c_scrn_rect.width,
                                    c_scrn_rect.height,
                                    )
                                   )

        c_txt_rect = Rect(c_scrn_rect.left + int(box_1.get_width() / 20),
                          c_scrn_rect.top + int(box_1.get_height() / 4),
                          box_1.get_width() - int(c_scrn_rect.width / 20),
                          box_1.get_height() - int(c_scrn_rect.height / 5))

        word_wrap(self._screen, c_txt_rect, self._combat_text, self._game_loop.display_info.text_font, (0, 0, 0))

        self._screen.blit(box_1, c_scrn_rect)
