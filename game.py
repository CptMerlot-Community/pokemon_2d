import pygame as pg
from pygame import freetype
import random
import time

random.seed(time.time_ns())


pg.init()
freetype.init()


def main():
    from game.render.display_info import configure_display, DISPLAY_INFO
    dp = configure_display(DISPLAY_INFO.R_960_720)

    from game.loop import GameLoop

    clock = pg.time.Clock()

    g = GameLoop(clock, dp)
    g.game_loop()


main()
