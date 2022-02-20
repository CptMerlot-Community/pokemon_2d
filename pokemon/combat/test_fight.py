import pytest
from pokemon.base.base import Pokemon, PokemonSchema, Base
from .fight import Combat


@pytest.fixture
def player_pokemon() -> Pokemon:
    poke = PokemonSchema(1, "test_pokemon", ["grass", "rock"],
                         Base(10, 20, 30, 30, 30, 20)
                         )
    return Pokemon(poke, (5, 5))


@pytest.fixture
def computer_pokemon() -> Pokemon:
    poke = PokemonSchema(1, "test_pokemon", ["grass", "rock"],
                         Base(10, 20, 30, 30, 30, 20)
                         )
    return Pokemon(poke, (1, 1))


def test_current_pokemon_logic(player_pokemon, computer_pokemon):
    c = Combat(player_pokemon, computer_pokemon)
    assert c._current_turn == c._player_pokemon


def test_combat_attack_phase(player_pokemon, computer_pokemon):
    c = Combat(player_pokemon, computer_pokemon)
    assert c._current_turn == c._player_pokemon
    c.attack()
    assert c._current_turn == c._computer_pokemon
    c.attack()
    assert c._current_turn == c._player_pokemon
    c.attack()
    assert c._current_turn == c._computer_pokemon
    c.attack()
    assert c._current_turn == c._player_pokemon
