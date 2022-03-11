from dataclasses import dataclass
import pygame as pg
from pygame import freetype
import random
import time

random.seed(time.time_ns())

# TODO: Move Sizing Options to Dataclass for all sizing needs
# @dataclass
# class ScreenSize:
#     Size = pg.Vector2(640, 480)
#     detail_font_size = 10
#     talk_text_font_size = 30

# SCREEN_SIZE = pg.Vector2(640, 480)
SCREEN_SIZE = pg.Vector2(800, 600)
# SCREEN_SIZE = pg.Vector2(960, 720)
# SCREEN_SIZE = pg.Vector2(1280, 960)

pg.init()
freetype.init()

clock = pg.time.Clock()
screen = pg.display.set_mode(SCREEN_SIZE)


def main():
    from game.loop import GameLoop
    g = GameLoop(screen, clock)
    g.game_loop()


main()
