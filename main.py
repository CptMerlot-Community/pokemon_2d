from pokemon.pokemons import GeneratePokemon
import random
import time

random.seed(time.time_ns())


f1 = GeneratePokemon(l_range=(1, 5), pokemons=[2])
print(f1)

print(f1.get_stats())
