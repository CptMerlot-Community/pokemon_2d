from dataclasses import dataclass
from typing import Tuple
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
                 talk_text_font_size: int,
                 welcome_font_size: int):
        self._pg_vector = vector
        self._details_font_size = details_size
        self._talk_text_font_size = talk_text_font_size

        self._details_font = pg.font.Font("assets/fonts/dogicapixel.ttf", self._details_font_size)
        self._details_font.bold = False

        self._text_font = FFont(file="assets/fonts/dogicapixel.ttf", size=self._talk_text_font_size)

        self._welcome_font = pg.font.SysFont("Arial", welcome_font_size)
        self._welcome_font.bold = True
        self.screen = pg.display.set_mode(self._pg_vector)

        self.select_pokemon_arrow: Tuple[float, float] = self.width*.03, self.height*.048
        self.pokemon_size: Tuple[float, float] = self.width/3, self.height / 2.5
        self.detail_size: Tuple[float, float] = self.width/2.5, self.height/5.5
        self.pokemon_screen_select_pokemon_rect_size: Tuple[float, float, float, float] = (self.width * .20,
                                                                                           self.height * .02,
                                                                                           self.width,
                                                                                           self.height/10)
        self.detail_text_start_left_mod = .30
        self.detail_text_start_bottom_mod = .15
        self.hp_bar_width = self.width * .20
        self._combat_window_height = .30

        self.color_white_rbg = 255, 255, 255
        self.color_off_white_rbg = 220, 220, 220
        self.color_black_rbg = 0, 0, 0

    @property
    def combat_window_height(self) -> float:
        return self._combat_window_height

    @property
    def width(self) -> int:
        return self.screen.get_width()

    @property
    def height(self) -> int:
        return self.screen.get_height()

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


def configure_display(display_info: DISPLAY_INFO) -> DisplayInfo:
    # TODO: Remove passing in sizes instead do base
    # values and multiple by the correct scaling percentages per the resolution
    if display_info.value == DISPLAY_INFO.R_480_640.value:
        return DisplayInfo(pg.Vector2(640, 480), 18, 28, 40)
    elif display_info.value == DISPLAY_INFO.R_800_600.value:
        return DisplayInfo(pg.Vector2(800, 600), 22, 35, 50)
    elif display_info.value == DISPLAY_INFO.R_960_720.value:
        return DisplayInfo(pg.Vector2(960, 720), 28, 50, 60)
    elif display_info.value == DISPLAY_INFO.R_1280_960.value:
        return DisplayInfo(pg.Vector2(1280, 960), 40, 60, 80)
    else:
        return DisplayInfo(pg.Vector2(640, 480), 18, 28, 40)
