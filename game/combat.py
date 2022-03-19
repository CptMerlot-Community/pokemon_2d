from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Tuple
import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect
from pokemon.base.pokemon import Pokemon
from pokemon.pokemons import GeneratePokemon
from pokemon.combat.fight import Combat
from game.render.fonts import word_wrap  # type: ignore
from game.battle.pokemon_select import PokemonSelectScreen  # type: ignore
from game.battle.player_action import PlayerAction  # type: ignore
from game.battle.details_screen import DetailsScreen, box2, arrow_right  # type: ignore
from game.battle.new_combat_screen import CombatStart  # type: ignore


if TYPE_CHECKING:
    from .loop import GameLoop


class CombatScreen():
    _fainted_pokemon: Optional[Pokemon] = None
    _pokemon_selector_screen: Optional[PokemonSelectScreen] = None
    _player_turn = False
    _new_combat = True

    # Phase of combat tracker
    # New Comabt - Done
    # # Render in Pokemon + Player (Scroll Across Screen) <- Kind of did this
    # ## Wild Pokemon <-- blocks for enter key <-- Kind of did this
    # ## GO! XYZ! <--- need to do this
    # Than Combat <-- blocking action
    # # Prompt Player for Action
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
        self._battle_details_screen: DetailsScreen = DetailsScreen(self)
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
        self.set_combat_text(f"A wild {self._combat._computer_pokemon.name} has appeared.")

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

        if self._new_combat:
            self._battle_details_screen.combat_text_render()
            self._combat_start.render()
        elif self._pokemon_selector_screen is not None:
            self._pokemon_selector_screen.render()
        elif self._player_turn:
            self._player_action_screen.render()
        else:
            self._battle_details_screen.render_full_battle_screen()

            # Get Event Loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_loop.StopRunning()
                if self._fainted_pokemon is not None:
                    if event.type == pg.KEYDOWN:
                        if event.key in (pg.K_RETURN, pg.K_SPACE, pg.K_ESCAPE):
                            if self._fainted_pokemon is self.game_loop.player.active_pokemon:
                                if not self.game_loop.player.check_if_available_pokemons():
                                    self.game_loop.GameOver(True)
                                else:
                                    self.pokemon_select_screen()
                            else:
                                self.game_loop.ExitCombat()
                else:
                    if event.type == pg.KEYDOWN:
                        if event.key in (pg.K_RETURN, pg.K_SPACE):
                            attk_pokemon = self._combat.attack_pokemon.name
                            def_pokemon = self._combat.defending_pokemon.name
                            self.set_combat_text(
                                f"{attk_pokemon} hits {def_pokemon} for {self._combat.attack()}")
                            self._fainted_pokemon = self._combat.pokemon_fainted()
                            if self._fainted_pokemon is not None:
                                self.set_combat_text(
                                    f"{self._fainted_pokemon.name} has fainted...")
                        if event.key == pg.K_ESCAPE:
                            self.game_loop.StopRunning()
