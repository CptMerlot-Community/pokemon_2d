# Learning OOP Principals with Python while building a Pokemon game

> The goal of this was original to teach some OOP principals but than we ADHDed ourselves into creating a 2d Python game using PyGame of a Pokemon inspired game.

# hp\attk\def\speed mod algo
* hp base * (level * mod)
*  40 * (20 * .22) = 176

# attack rules

* attack_algo
* highest spd attacks
* unless preemptive encounter

## Combat Damage

* Roll for hit
    * Base Roll - (level diff - (Atk Level Mob - Def Level Mob)) / Random Ranged Value[1-20] 
* Roll for damage
    * (base DMG Roll * (mod Atking Base Attk - Defending Base Def)) * (Weak mod_range[30-50] or Effective mod_range[30-40])
