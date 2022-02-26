import pytest
from pokemon.base.base import Pokemon, PokemonSchema, Base, Name
from .fight import Combat
from pokemon.pokemons import _load_pokemon_types


@pytest.fixture
def player_pokemon() -> Pokemon:

    pt = _load_pokemon_types(["grass", "rock"])
    poke = PokemonSchema(1, Name("test_pokemon"), pt,
                         Base(10, 20, 30, 30, 30, 20)
                         )
    return Pokemon(poke, (6, 6))


@pytest.fixture
def computer_pokemon() -> Pokemon:
    pt = _load_pokemon_types(["grass", "rock"])
    poke = PokemonSchema(1, Name("test_pokemon"), pt,
                         Base(10, 20, 30, 30, 30, 20)
                         )
    return Pokemon(poke, (5, 5))


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
