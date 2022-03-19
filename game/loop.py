from typing import Optional
import pygame as pg
from pygame.time import Clock
from pygame.surface import Surface
from game.main import MainScreen
from game.combat import CombatScreen
from game.render.display_info import DisplayInfo  # type: ignore
from pokemon.base.player import Player
from pokemon.combat.fight import Combat
from pokemon.pokemons import GeneratePokemon


class GameLoop():
    def __init__(self, clock: Clock, display_info: DisplayInfo):
        self._running = True
        self._screen = display_info.screen
        self._current_battle = False
        self._game_over = False
        self._clock = clock
        self._clock_tick_rate = 60
        self.display_info = display_info
        self.player: Player = Player(name="CptMerlot")
        self.player.add_pokemon(GeneratePokemon(l_range=(4, 4), pokemons=[25]))
        self.player.add_pokemon(GeneratePokemon(l_range=(4, 4), pokemons=[1]))
        self.player.add_pokemon(GeneratePokemon(l_range=(4, 4), pokemons=[4]))
        self._c: Optional[CombatScreen] = None
        self._w = MainScreen(self._screen, self)

    def EnterCombat(self):
        c1 = GeneratePokemon(l_range=(4, 4), pokemons=[1, 4, 19, 43])
        self._c = CombatScreen(self._screen, self, combat=Combat(self.player.active_pokemon, c1))

    def ExitCombat(self):
        self._c = None

    def StopRunning(self):
        self._running = False

    def GameOver(self, b: bool):
        self._game_over = b

    def game_loop(self):
        while self._running:
            if self._game_over:
                self._w.game_over_render()
            elif self._c is not None:
                self._c.render()
            else:
                self._w.welcome_render()

            pg.display.update()
            self._clock.tick(self._clock_tick_rate)

        pg.quit()
