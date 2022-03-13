import pytest
from .pokemon import PokemonSchema, Base, Pokemon


@pytest.fixture
def pokemon_test_lvl_5():
    poke = PokemonSchema(1, "test_pokemon", ["grass", "rock"],
                         Base(10, 20, 30, 30, 30, 20)
                         )
    return Pokemon(poke, (5, 5))


def test_base_stat_generates(pokemon_test_lvl_5: Pokemon):
    assert pokemon_test_lvl_5._attk_pw == 10
    assert pokemon_test_lvl_5._defense == 15
    assert pokemon_test_lvl_5._hitpoints == 15
    assert pokemon_test_lvl_5._speed == 10


def test_get_base_stats(pokemon_test_lvl_5: Pokemon):
    stats = pokemon_test_lvl_5.get_stats()
    assert stats['attack'] == 10
    assert stats['defense'] == 15
    assert stats['hitpoints'] == 15
    assert stats['speed'] == 10
    assert stats['level'] == 5
    assert stats['experience'] == 0


def test_level_up(pokemon_test_lvl_5: Pokemon):
    assert pokemon_test_lvl_5._attk_pw == 10
    assert pokemon_test_lvl_5._defense == 15
    assert pokemon_test_lvl_5._hitpoints == 15
    assert pokemon_test_lvl_5._speed == 10

    pokemon_test_lvl_5.level_up()

    assert pokemon_test_lvl_5._level == 6
    assert pokemon_test_lvl_5._attk_pw == 12
    assert pokemon_test_lvl_5._defense == 18
    assert pokemon_test_lvl_5._hitpoints == 18
    assert pokemon_test_lvl_5._speed == 12


def test_take_damage(pokemon_test_lvl_5: Pokemon):
    pokemon_test_lvl_5.take_damage(4)
    assert pokemon_test_lvl_5.alive is True
    assert pokemon_test_lvl_5._current_hitpoints == 11
    assert pokemon_test_lvl_5._hitpoints == 15
    pokemon_test_lvl_5.take_damage(2)
    assert pokemon_test_lvl_5.alive is True
    assert pokemon_test_lvl_5._current_hitpoints == 9
    assert pokemon_test_lvl_5._hitpoints == 15
    pokemon_test_lvl_5.take_damage(10)
    assert pokemon_test_lvl_5.alive is False
    assert pokemon_test_lvl_5._current_hitpoints == 0
    assert pokemon_test_lvl_5._hitpoints == 15


def test_no_positive_take_damage(pokemon_test_lvl_5: Pokemon):
    pokemon_test_lvl_5.take_damage(2)
    assert pokemon_test_lvl_5.alive is True
    assert pokemon_test_lvl_5._current_hitpoints == 13
    pokemon_test_lvl_5.take_damage(-2)
    assert pokemon_test_lvl_5._current_hitpoints == 13


def test_healing(pokemon_test_lvl_5: Pokemon):
    pokemon_test_lvl_5.take_damage(2)
    assert pokemon_test_lvl_5.alive is True
    pokemon_test_lvl_5.heal(-2)
    assert pokemon_test_lvl_5._current_hitpoints == 13
    pokemon_test_lvl_5.heal(1)
    assert pokemon_test_lvl_5._current_hitpoints == 14
    pokemon_test_lvl_5.heal(5)
    assert pokemon_test_lvl_5._current_hitpoints == 15
    pokemon_test_lvl_5.heal(1)
    assert pokemon_test_lvl_5._current_hitpoints == 15
