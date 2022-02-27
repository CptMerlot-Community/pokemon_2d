from cgi import test
import pygame as pg
from pygame.surface import Surface
from pokemon.pokemons import GeneratePokemon
from pokemon.combat.fight import Combat
import random
import time
import os

random.seed(time.time_ns())

SCREEN_SIZE = pg.Vector2(800, 400)

pg.init()
clock = pg.time.Clock()
white = 255, 255, 255

combat_window_height = .22
screen = pg.display.set_mode(SCREEN_SIZE)

pokemon_stat_font = pg.font.SysFont("Arial", 20)
pokemon_stat_font.bold = False

welcome_font = pg.font.SysFont("Arial", 40)
welcome_font.bold = True

running = True
current_combat = False
combat_text = ""


def start_new_combat() -> Combat:
    p1 = GeneratePokemon(l_range=(4, 4), pokemons=[1, 19, 43])
    print(p1)
    c1 = GeneratePokemon(l_range=(4, 4), pokemons=[1, 19, 43])
    print(c1)
    return Combat(p1, c1)


c = start_new_combat()


def attack_screen(scn: Surface):
    global c
    global running
    global combat_text
    winning_pokemon = c.winning_pokemon()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if winning_pokemon is not None:
            combat_text = f"{winning_pokemon.name} has won"
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_RETURN, pg.K_SPACE, pg.K_ESCAPE):
                    c = start_new_combat()
                    combat_text = ""
        else:
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_RETURN, pg.K_SPACE):
                    attk_pokemon = c.attack_pokemon.name
                    def_pokemon = c.defending_pokemon.name
                    dmg = c.attack()
                    combat_text = f"{attk_pokemon} hits {def_pokemon} for {dmg}"
                if event.key == pg.K_ESCAPE:
                    c = start_new_combat()
                    combat_text = ""

    scn.fill((0, 0, 0))
    # player pokemon
    pg.draw.rect(scn, (255, 0, 0), (60, 225, 200, 75))

    # player detail scn
    p_detail = pg.rect.Rect((530, 200, 225, 100))
    # pg.draw.rect(scn, (255, 255, 255), )
    scn.fill((255, 255, 255), p_detail)

    # enemy pokemon
    pg.draw.rect(scn, (0, 0, 255), (530, 50, 200, 75))

    # enemy detail scn
    e_detail = pg.rect.Rect((30, 20, 200, 75))
    # pg.draw.rect(scn, (255, 255, 255), (30, 20, 200, 75))
    scn.fill((255, 255, 255), e_detail)

    # TODO: This trash.com this needs to be done a better way
    p_level = pokemon_stat_font.render(f"Level: {c._player_pokemon.level}", False, (111, 196, 169))
    p_level_rect = p_level.get_rect(center=(p_detail.centerx, p_detail.top + 30))
    p_hp = pokemon_stat_font.render(f"HP: {c._player_pokemon.current_hitpoints} / {c._player_pokemon.hitpoints}",
                                    False, (111, 196, 169))
    p_hp_rect = p_hp.get_rect(center=(p_detail.centerx, p_detail.bottom - 30))
    p_name = pokemon_stat_font.render(f"{c._player_pokemon.name}", False, (111, 196, 169))
    p_name_rect = p_name.get_rect(center=(p_detail.centerx, p_detail.top + 10))

    e_level = pokemon_stat_font.render(f"Level: {c._computer_pokemon.level}", False, (111, 196, 169))
    e_level_rect = e_level.get_rect(center=(e_detail.centerx, e_detail.top + 25))
    e_hp = pokemon_stat_font.render(f"HP: {c._computer_pokemon.current_hitpoints} / {c._computer_pokemon.hitpoints}",
                                    False, (111, 196, 169))
    e_hp_rect = e_hp.get_rect(center=(e_detail.centerx, e_detail.bottom - 20))
    e_name = pokemon_stat_font.render(f"{c._computer_pokemon.name}", False, (111, 196, 169))
    e_name_rect = e_name.get_rect(center=(e_detail.centerx, e_detail.top + 10))

    scn.blit(p_hp, p_hp_rect)
    scn.blit(p_name, p_name_rect)
    scn.blit(p_level, p_level_rect)

    scn.blit(e_hp, e_hp_rect)
    scn.blit(e_name, e_name_rect)
    scn.blit(e_level, e_level_rect)

    # combat screen
    c_scrn_rect = pg.draw.rect(scn,
                               (255, 255, 255),
                               (0,
                                scn.get_height()-(scn.get_height()*combat_window_height),
                                scn.get_width(),
                                scn.get_height()*combat_window_height
                                )
                               )
    c_txt = welcome_font.render(combat_text, False, (0, 0, 0))
    c_txt_rect = c_txt.get_rect(center=c_scrn_rect.center)
    scn.blit(c_txt, c_txt_rect)


def welcome_render(scn: Surface):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            global running
            running = False
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_RETURN, pg.K_SPACE):
                global current_combat
                current_combat = True

    scn.fill((0, 0, 0))
    wf = welcome_font.render("Welcome to Pokemon 2d", False, (255, 255, 255))
    wf_rect = wf.get_rect(center=(scn.get_width() / 2, scn.get_height() / 2))
    scn.blit(wf, wf_rect)


while running:
    if current_combat:
        attack_screen(screen)
    else:
        welcome_render(screen)

    pg.display.update()
    clock.tick(60)

pg.quit()
