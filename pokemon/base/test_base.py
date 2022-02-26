import pytest
from .base import PokemonSchema, Base, Pokemon


@pytest.fixture
def pokemon_test_lvl_5():
    poke = PokemonSchema(1, "test_pokemon", ["grass", "rock"],
                         Base(10, 20, 30, 30, 30, 20)
                         )
    return Pokemon(poke, (5, 5))


def test_base_stat_rolls(pokemon_test_lvl_5: Pokemon):
    assert pokemon_test_lvl_5._attk_pw == 100
    assert pokemon_test_lvl_5._defense == 150
    assert pokemon_test_lvl_5._hitpoints == 50
    assert pokemon_test_lvl_5._speed == 100


def test_get_base_stats(pokemon_test_lvl_5: Pokemon):
    stats = pokemon_test_lvl_5.get_stats()
    assert stats['attack'] == 100
    assert stats['defense'] == 150
    assert stats['hitpoints'] == 50
    assert stats['speed'] == 100
    assert stats['level'] == 5
    assert stats['experience'] == 0


def test_level_up(pokemon_test_lvl_5: Pokemon):
    assert pokemon_test_lvl_5._attk_pw == 100
    assert pokemon_test_lvl_5._defense == 150
    assert pokemon_test_lvl_5._hitpoints == 50
    assert pokemon_test_lvl_5._speed == 100

    pokemon_test_lvl_5.level_up()

    assert pokemon_test_lvl_5._level == 6
    assert pokemon_test_lvl_5._attk_pw == 120
    assert pokemon_test_lvl_5._defense == 180
    assert pokemon_test_lvl_5._hitpoints == 60
    assert pokemon_test_lvl_5._speed == 120


def test_take_damage(pokemon_test_lvl_5: Pokemon):
    pokemon_test_lvl_5.take_damage(10)
    assert pokemon_test_lvl_5.alive is True
    assert pokemon_test_lvl_5._current_hitpoints == 40
    assert pokemon_test_lvl_5._hitpoints == 50
    pokemon_test_lvl_5.take_damage(6)
    assert pokemon_test_lvl_5.alive is True
    assert pokemon_test_lvl_5._current_hitpoints == 34
    assert pokemon_test_lvl_5._hitpoints == 50
    pokemon_test_lvl_5.take_damage(40)
    assert pokemon_test_lvl_5.alive is False
    assert pokemon_test_lvl_5._current_hitpoints == 0
    assert pokemon_test_lvl_5._hitpoints == 50


def test_no_positive_take_damage(pokemon_test_lvl_5: Pokemon):
    pokemon_test_lvl_5.take_damage(10)
    assert pokemon_test_lvl_5.alive is True
    pokemon_test_lvl_5.take_damage(-10)
    assert pokemon_test_lvl_5._current_hitpoints == 40


def test_healing(pokemon_test_lvl_5: Pokemon):
    pokemon_test_lvl_5.take_damage(10)
    assert pokemon_test_lvl_5.alive is True
    pokemon_test_lvl_5.heal(-10)
    assert pokemon_test_lvl_5._current_hitpoints == 40
    pokemon_test_lvl_5.heal(5)
    assert pokemon_test_lvl_5._current_hitpoints == 45
    pokemon_test_lvl_5.heal(10)
    assert pokemon_test_lvl_5._current_hitpoints == 50
    pokemon_test_lvl_5.heal(1)
    assert pokemon_test_lvl_5._current_hitpoints == 50
