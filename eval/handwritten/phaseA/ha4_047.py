# A knight walks into a clearing and meets three wolves.
# All wolves start with the same health. Each round the knight strikes,
# and every wolf still standing bites for 4 minus the knight's armor.

wolf1 = wolf2 = wolf3 = 30
knight = 100
sword = 13
armor = 1

print("Round 1: wolf 1")
wolf1 -= sword
knight -= 3 * (4 - armor)
print(wolf1)
print(knight)

print("Round 2: wolf 1")
wolf1 -= sword
knight -= 3 * (4 - armor)
print(wolf1)
print(knight)

print("Round 3: sweeping blow")
# half damage to every wolf
wolf1 -= sword // 2
wolf2 -= sword // 2
wolf3 -= sword // 2
# wolf 1 is down; two wolves bite
knight -= 2 * (4 - armor)
print(wolf1)
print(knight)

print("Round 4: wolf 2")
wolf2 -= sword
knight -= 2 * (4 - armor)
print(wolf2)
print(knight)

print("Round 5: shield found")
armor += 2
wolf2 -= sword
knight -= 4 - armor
print(wolf2)
print(knight)

print("Round 6: wolf 3")
wolf3 -= sword
knight -= 4 - armor
print(wolf3)

print("Round 7: wolf 3")
wolf3 -= sword
print(wolf3)

print("--- clearing ---")
print(knight)
# overkill: how far below zero the wolves went in total
print(-(wolf1 + wolf2 + wolf3))
