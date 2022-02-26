from typing import Tuple, List, Dict, Any
import random
import json

from pokemon.base.base import Pokemon, PokemonSchema, Base, Type

POKEMON_DATA_LOCATION = "C:\\Users\\cptme\\Documents\\Code\\OOP\\pokemon_2d\\data\\pokemon.json"
POKEMON_TYPE_DATA_LOCATION = "C:\\Users\\cptme\\Documents\\Code\\OOP\\pokemon_2d\\data\\pokemon_type.json"

POKEMON_DATA: List[Dict[str, Any]] = []
POKEMON_TYPE_DATA: List[Dict[str, Any]] = []


# TODO: Change Pokemon Data to a Dict of PokemonSchema where key is the Pokemon ID
# TODO: Attach Pokemon Type information at the load time of the creation of POKEMON_DATA
def _load_pokemon_data():
    global POKEMON_DATA
    global POKEMON_TYPE_DATA
    f = open(POKEMON_DATA_LOCATION, "r", encoding="utf8")
    POKEMON_DATA = json.loads(f.read())

    f = open(POKEMON_TYPE_DATA_LOCATION, "r", encoding="utf8")
    POKEMON_TYPE_DATA = json.loads(f.read())


_load_pokemon_data()


# TODO: Prevent rolling for pokemon below the required level thresholds or way lower than required level
def GeneratePokemon(l_range: Tuple[int, int], pokemons: List[int]):
    # level = random.randint(l_range[0], l_range[1])
    pokemon_id = pokemons[random.randint(0, len(pokemons) - 1)]
    pokemon_schema = _load_pokemon_from_data(pokemon_id)
    return Pokemon(pokemon_schema, level_range=l_range)


def _load_pokemon_from_data(pokemon_id: int) -> PokemonSchema:
    p = POKEMON_DATA[pokemon_id - 1]
    p_type = _load_pokemon_types(p['type'])
    return PokemonSchema(
                         p['id'],
                         p['name']['english'],
                         p_type,
                         Base(
                             p['base']['HP'],
                             p['base']['Attack'],
                             p['base']['Defense'],
                             p['base']['Sp. Attack'],
                             p['base']['Sp. Defense'],
                             p['base']['Speed'],
                             ),
                         )


def _load_pokemon_types(pokemon_types: List[str]) -> Type:
    weak = []
    strong = []
    resistant = []
    vulnerable = []
    for type in pokemon_types:
        if type in POKEMON_TYPE_DATA:
            info = POKEMON_TYPE_DATA[type]
            if "Weak" in info:
                info = info["Weak"]
                for i in info:
                    if i not in weak:
                        weak.append(i)
            if "Strong" in info:
                info = info["Strong"]
                for i in info:
                    if i not in weak:
                        strong.append(i)
            if "Resistant" in info:
                info = info["Resistant"]
                for i in info:
                    if i not in weak:
                        resistant.append(i)
            if "Vulnerable" in info:
                info = info["Vulnerable"]
                for i in info:
                    if i not in weak:
                        vulnerable.append(i)
    return Type(pokemon_types, weak, strong, resistant, vulnerable)
