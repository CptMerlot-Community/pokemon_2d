import pygame as pg
from pygame.time import Clock
from pygame.surface import Surface
from game.main import MainScreen
from .combat import CombatScreen
from .render.display_info import DisplayInfo


class GameLoop():
    def __init__(self, screen: Surface, clock: Clock, display_info: DisplayInfo):
        self._running = True
        self._screen = screen
        self._current_combat = False
        self._clock = clock
        self.display_info = display_info
        self._c = CombatScreen(self._screen, self)
        self._w = MainScreen(self._screen, self)
        self._clock_tick_rate = 60

    def StopRunning(self):
        self._running = False

    def Combat(self):
        self._current_combat = True

    def game_loop(self):
        while self._running:
            if self._current_combat:
                self._c.attack_screen()
            else:
                self._w.welcome_render()

            pg.display.update()
            self._clock.tick(self._clock_tick_rate)

        pg.quit()
