from typing import Tuple, List
import random

from pokemon.base.base import Pokemon


# TODO: Prevent rolling for pokemon below the required level thresholds or way lower than required level
def GeneratePokemon(l_range: Tuple[int, int], pokemons: List[Pokemon]):
    # level = random.randint(l_range[0], l_range[1])
    pokemon = pokemons[random.randint(0, len(pokemons) - 1)]

    return pokemon(level_range=l_range)
