from .pokemons import _load_pokemon_types

def test_unknown_type_pokemon_data():
    t = _load_pokemon_types(["unknown"])
    assert len(t.type) == 0
    assert len(t.resistant) == 0
    assert len(t.vulnerable) == 0
    assert len(t.weak) == 0
    assert len(t.strong) == 0

def test_single_type_pokemon_data():
    t = _load_pokemon_types(["grass"])
    assert len(t.type) == 1
    assert len(t.resistant) == 4
    assert len(t.vulnerable) == 5
    assert len(t.weak) == 7
    assert len(t.strong) == 3

def test_multi_type_pokemon_data():
    t = _load_pokemon_types(["grass", "Poison"])
    assert len(t.type) == 2
    assert len(t.resistant) == 7
    assert len(t.vulnerable) == 7
    assert len(t.weak) == 10
    assert len(t.strong) == 5