from pokemon.pokemons import GeneratePokemon
from pokemon.combat.fight import Combat
import random
import time

random.seed(time.time_ns())


p1 = GeneratePokemon(l_range=(3, 4), pokemons=[1])
print(p1)

c1 = GeneratePokemon(l_range=(1, 2), pokemons=[1])
print(c1)

c = Combat(p1, c1)
while c.is_combat_over() is not True:
    c.attack()


print("")
