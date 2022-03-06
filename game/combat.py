from __future__ import annotations
from typing import TYPE_CHECKING
import pygame as pg
from pygame.surface import Surface
from pokemon.pokemons import GeneratePokemon
from pokemon.combat.fight import Combat

if TYPE_CHECKING:
    from .loop import GameLoop

pokemon_stat_font = pg.font.SysFont("Arial", 20)
pokemon_stat_font.bold = False

combat_text_format = pg.font.SysFont("Arial", 25)

combat_window_height = .22

white = 255, 255, 255
off_white = 220, 220, 220

box1 = pg.image.load("./assets/BOX_1.png").convert_alpha()
box2 = pg.image.load("./assets/BOX_2.png").convert_alpha()

pLine = pg.image.load("./assets/LINE_1.png").convert_alpha()
eLine = pg.image.load("./assets/LINE_2.png").convert_alpha()

p_pokemon = pg.image.load("./assets/Character_11_seafoam.png").convert_alpha()
e_pokemon = pg.image.load("./assets/Character_9_baby_pink.png").convert_alpha()


class CombatScreen():
    _combat: Combat

    def __init__(self, screen: Surface, game_loop: GameLoop):
        self._screen = screen
        self._combat_text = ""
        self._game_loop = game_loop
        self.start_new_combat()

    def start_new_combat(self):
        p1 = GeneratePokemon(l_range=(4, 4), pokemons=[25])
        c1 = GeneratePokemon(l_range=(4, 4), pokemons=[1, 4, 19, 43])
        self._combat = Combat(p1, c1)
        self._combat_text = ""

    def attack_screen(self):
        winning_pokemon = self._combat.winning_pokemon()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._game_loop.StopRunning()
            if winning_pokemon is not None:
                self._combat_text = f"{winning_pokemon.name} has won"
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
                    if event.key == pg.K_ESCAPE:
                        self.start_new_combat()

        self._screen.fill(off_white)

        # combat screen
        c_scrn_rect = pg.draw.rect(self._screen,
                                   (off_white),
                                   (0,
                                    int(self._screen.get_height()-(self._screen.get_height()*combat_window_height)),
                                    self._screen.get_width(),
                                    int(self._screen.get_height()*combat_window_height)
                                    )
                                   )

        # player pokemon
        p_pokemon_rect = pg.rect.Rect((c_scrn_rect.left + int(self._screen.get_width()/10),
                                      self._screen.get_height()/2.1,
                                      self._screen.get_width()/3,
                                      self._screen.get_height()/2.5))
        p_poke = pg.transform.scale(p_pokemon, (p_pokemon_rect.width, p_pokemon_rect.height))
        self._screen.blit(p_poke, p_pokemon_rect.topleft)

        # player detail scn
        p_detail = pg.rect.Rect((c_scrn_rect.right / 2,
                                 self._screen.get_height()/2,
                                 self._screen.get_width()/2,
                                 self._screen.get_height()/3.5))

        # enemy pokemon
        e_pokemon_rect = pg.rect.Rect((c_scrn_rect.right - int(self._screen.get_width()/2.7),
                                      self._screen.get_height()/20,
                                      self._screen.get_width()/3,
                                      self._screen.get_height()/2.5))
        e_poke = pg.transform.scale(e_pokemon,  (e_pokemon_rect.width, e_pokemon_rect.height))
        self._screen.blit(e_poke, e_pokemon_rect.topleft)

        # enemy detail scn
        e_detail = pg.rect.Rect((c_scrn_rect.left + (self._screen.get_width()/50),
                                self._screen.get_height()/20,
                                self._screen.get_width()/2.5,
                                self._screen.get_height()/5.5))

        # TODO: This trash.com this needs to be done a better way
        p_name = pokemon_stat_font.render(f"{self._combat._player_pokemon.name}", False, (111, 196, 169))
        p_name_rect = p_name.get_rect(center=(p_detail.centerx, p_detail.top + (p_detail.height * .10)))
        p_level = pokemon_stat_font.render(f"L:{self._combat._player_pokemon.level}", False, (111, 196, 169))
        p_level_rect = p_level.get_rect(midtop=p_name_rect.midbottom)
        p_hp = pokemon_stat_font.render("HP: {0} / {1}".format(
                                                               self._combat._player_pokemon.current_hitpoints,
                                                               self._combat._player_pokemon.hitpoints),
                                        False, (111, 196, 169))
        p_hp_rect = p_hp.get_rect(centerx=p_detail.centerx, bottom=p_detail.bottom - (p_detail.height * .21))

        e_name = pokemon_stat_font.render(f"{self._combat._computer_pokemon.name}", False, (111, 196, 169))
        e_name_rect = e_name.get_rect(center=(e_detail.centerx, e_detail.top + (e_detail.height * .10)))
        e_level = pokemon_stat_font.render(f"L:{self._combat._computer_pokemon.level}", False, (111, 196, 169))
        e_level_rect = e_level.get_rect(midtop=e_name_rect.midbottom)
        e_hp = pokemon_stat_font.render("HP: {0} / {1}".format(
                                                               self._combat._computer_pokemon.current_hitpoints,
                                                               self._combat._computer_pokemon.hitpoints),
                                        False, (111, 196, 169))
        e_hp_rect = e_hp.get_rect(centerx=e_detail.centerx, bottom=e_detail.bottom - (e_detail.height * .10))

        self._screen.blit(p_hp, p_hp_rect)
        self._screen.blit(p_name, p_name_rect)
        self._screen.blit(p_level, p_level_rect)

        self._screen.blit(e_hp, e_hp_rect)
        self._screen.blit(e_name, e_name_rect)
        self._screen.blit(e_level, e_level_rect)
        e_line = pg.transform.scale(eLine, (e_detail.width, e_detail.height))
        p_line = pg.transform.scale(pLine, (p_detail.width * .80, p_detail.height * .80))
        # TODO:  See if there is a way to put line inside a rect and have it join on the bottom right of the detail rect
        self._screen.blit(p_line, (p_detail.left + int(p_detail.left * .15), p_detail.top + int(p_detail.top * .15)))
        self._screen.blit(e_line, e_detail.topleft)

        box_1 = pg.transform.scale(box1,
                                   (c_scrn_rect.width + int(c_scrn_rect.width / 100),
                                    c_scrn_rect.height + int(c_scrn_rect.height / 100)
                                    )
                                   )
        c_txt = combat_text_format.render(self._combat_text, False, (0, 0, 0))
        c_txt_rect = c_txt.get_rect(left=c_scrn_rect.left + int(c_scrn_rect.width / 20),
                                    top=c_scrn_rect.top + int(c_scrn_rect.height / 5))
        self._screen.blit(box_1, c_scrn_rect)
        self._screen.blit(c_txt, c_txt_rect)
