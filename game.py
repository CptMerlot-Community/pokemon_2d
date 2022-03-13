import pygame as pg
from pygame import freetype
import random
import time

random.seed(time.time_ns())


pg.init()
freetype.init()


def main():
    from game.render.display_info import get_display_info, DISPLAY_INFO
    dp = get_display_info(DISPLAY_INFO.R_1280_960)
    screen = pg.display.set_mode(dp.vector)

    from game.loop import GameLoop

    clock = pg.time.Clock()

    g = GameLoop(screen, clock, dp)
    g.game_loop()


main()
