from typing import Tuple, List, Dict, Any
import random

from pokemon.base.base import Pokemon, PokemonSchema, Base, Type
from pokemon.data import POKEMON_DATA, POKEMON_TYPE_DATA


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
    weak: List[str] = []
    strong: List[str] = []
    resistant: List[str] = []
    vulnerable: List[str] = []
    p_types: List[str] = []
    for pt in pokemon_types:
        pConvert = pt.capitalize()
        if pConvert in POKEMON_TYPE_DATA:
            p_types.append(pConvert)
            info = POKEMON_TYPE_DATA[pConvert]
            if "Weak" in info:
                info_weak = info["Weak"]
                for i in info_weak:
                    if i not in weak:
                        weak.append(i)
            if "Strong" in info:
                info_strong = info["Strong"]
                for i in info_strong:
                    if i not in strong:
                        strong.append(i)
            if "Resistant" in info:
                info_resistant = info["Resistant"]
                for i in info_resistant:
                    if i not in resistant:
                        resistant.append(i)
            if "Vulnerable" in info:
                info_vulnerable = info["Vulnerable"]
                for i in info_vulnerable:
                    if i not in vulnerable:
                        vulnerable.append(i)
    return Type(p_types, weak, strong, resistant, vulnerable)
