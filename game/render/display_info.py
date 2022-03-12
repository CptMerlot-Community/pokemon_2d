from dataclasses import dataclass
from attr import attributes
import pygame as pg
from pygame.freetype import Font as FFont  # type: ignore
from pygame.font import Font
from enum import Enum


@dataclass
class DisplayInfo:
    def __init__(self,
                 vector: pg.Vector2,
                 details_size: int,
                 talk_text_font_size: int):
        self._pg_vector = vector
        self._details_font_size = details_size
        self._talk_text_font_size = talk_text_font_size

        self._details_font = pg.font.Font("assets/fonts/dogicapixel.ttf", self._details_font_size)
        self._details_font.bold = False

        self._text_font = FFont(file="assets/fonts/dogicapixel.ttf", size=self._talk_text_font_size)

        self._welcome_font = pg.font.SysFont("Arial", 40)
        self._welcome_font.bold = True

    @property
    def vector(self) -> pg.Vector2:
        return self._pg_vector

    @property
    def details_font(self) -> Font:
        return self._details_font

    @property
    def text_font(self) -> FFont:
        return self._text_font

    @property
    def welcome_font(self) -> Font:
        return self._welcome_font


class DISPLAY_INFO(Enum):
    R_480_640 = 1
    R_800_600 = 2
    R_960_720 = 3
    R_1280_960 = 4


def get_display_info(display_info: DISPLAY_INFO) -> DisplayInfo:
    if display_info.value == DISPLAY_INFO.R_480_640.value:
        return DisplayInfo(pg.Vector2(640, 480), 18, 28)
    elif display_info.value == DISPLAY_INFO.R_800_600.value:
        return DisplayInfo(pg.Vector2(800, 600), 22, 35)
    elif display_info.value == DISPLAY_INFO.R_960_720.value:
        return DisplayInfo(pg.Vector2(960, 720), 28, 50)
    elif display_info.value == DISPLAY_INFO.R_1280_960.value:
        return DisplayInfo(pg.Vector2(1280, 960), 40, 60)
    else:
        return DisplayInfo(pg.Vector2(640, 480), 18, 28)
