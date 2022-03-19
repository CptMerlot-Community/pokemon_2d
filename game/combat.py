from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple
import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect
from pokemon.base.pokemon import Pokemon
from pokemon.pokemons import GeneratePokemon
from pokemon.combat.fight import Combat
from game.render.fonts import word_wrap  # type: ignore
from game.battle.pokemon_select import PokemonSelectScreen
from game.battle.player_action import PlayerAction
from game.battle.battle_screen import BattleScreen, box1, box2, arrow_right
from game.battle.new_combat_screen import CombatStart


if TYPE_CHECKING:
    from .loop import GameLoop


class CombatScreen():
    _fainted_pokemon: Optional[Pokemon] = None
    _pokemon_selector_screen: Optional[PokemonSelectScreen] = None
    _player_turn = False
    _new_combat = True

    # Phase of combat tracker
    # New Comabt - Done
    # # Render in Pokemon + Player (Scroll Across Screen)
    # ## Wild Pokemon <-- blocks for enter key
    # ## GO! XYZ!
    # Than Combat <-- blocking action
    # # Pokemon Fainted <-- blocking action
    # # Awared XP or\and select new pokemon <--- blocking action
    # # Check for level up <-- blocking action
    # ## Render new pokemon stats <-- blocking action
    # #  Check for evolve pokemon <-- blocking action (Do you want to evolve) <-- blocking action
    # Leave combat - Done

    def __init__(self, screen: Surface, game_loop: GameLoop, combat: Combat):
        self._screen = screen
        self._combat: Combat = combat
        self.game_loop = game_loop
        self._combat_text_screen_rect = self.create_combat_text_rect()
        self._combat_text = ""
        self._player_action_screen: PlayerAction = PlayerAction(self, box2, arrow_right)
        self._battle_screen: BattleScreen = BattleScreen(self, self._combat)
        self._combat_start: CombatStart = CombatStart(self)

    def create_combat_text_rect(self) -> Rect:
        return pg.draw.rect(self._screen,
                            (self.game_loop.display_info.color_off_white_rbg),
                            (-10,
                             int(self._screen.get_height()-(self._screen.get_height()
                                                            * self.game_loop.display_info.combat_window_height)),
                             self._screen.get_width(),
                             int(self._screen.get_height() *
                                 self.game_loop.display_info.combat_window_height)
                             )
                            )

    def combat_open_over(self):
        self._new_combat = False

    def pokemon_select_screen(self):
        self._pokemon_selector_screen = PokemonSelectScreen(self._screen, self, arrow_right)

    def set_combat_text(self, text: str):
        self._combat_text = text

    def add_selected_player_pokemon(self, pokemon_id: int):
        self.game_loop.player.get_pokemon(pokemon_id)
        if self._combat is not None:
            self._combat.send_in_new_player_pokemon(self.game_loop.player.active_pokemon)
            self._fainted_pokemon = self._combat.pokemon_fainted()
            self._pokemon_selector_screen = None

    def set_player_turn(self, bool=True):
        self._player_turn = bool

    def render(self):

        self._screen.fill(self.game_loop.display_info.color_off_white_rbg)

        # combat screen

        box_1 = pg.transform.scale(box1,
                                   (self._combat_text_screen_rect.width,
                                    self._combat_text_screen_rect.height,
                                    )
                                   )

        c_txt_rect = Rect(self._combat_text_screen_rect.left + int(box_1.get_width() / 20),
                          self._combat_text_screen_rect.top + int(box_1.get_height() / 4),
                          box_1.get_width() - int(self._combat_text_screen_rect.width / 20),
                          box_1.get_height() - int(self._combat_text_screen_rect.height / 5))

        word_wrap(self._screen, c_txt_rect, self._combat_text, self.game_loop.display_info.text_font, (0, 0, 0))

        self._screen.blit(box_1, self._combat_text_screen_rect)

        if self._new_combat:
            # Render the new combat scroll effect
            self._combat_start.render()
        elif self._pokemon_selector_screen is not None:
            self._pokemon_selector_screen.render()
        elif self._player_turn:
            self._player_action_screen.render()
        else:
            self._battle_screen.render()

        # TODO: have logic in setting players_turn
        # self._combat_screen.set_player_turn()
