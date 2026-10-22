# The final boss hides behind a magic shield.
# While the shield holds, it soaks up half of every hit (rounded down).
# The knight's sword gets 5 points sharper after every round.

boss_hp = 300
shield = 40
sword = 22
knight_hp = 90
boss_power = 13

print("Round 1")
absorbed = sword // 2
shield -= absorbed
boss_hp -= sword - absorbed
knight_hp -= boss_power
sword += 5
print(boss_hp)
print(shield)

print("Round 2")
absorbed = sword // 2
shield -= absorbed
boss_hp -= sword - absorbed
knight_hp -= boss_power
sword += 5
print(boss_hp)
print(shield)

print("Round 3")
absorbed = sword // 2
shield -= absorbed
boss_hp -= sword - absorbed
knight_hp -= boss_power
sword += 5
print(boss_hp)
print(shield)

print("The shield shatters!")
# the boss is furious and hits harder
boss_power += 5

print("Round 4")
boss_hp -= sword * 2
knight_hp -= boss_power
print(boss_hp)
print(knight_hp)

print("Round 5: elixir")
# the elixir doubles the knight's health before the hit
knight_hp *= 2
boss_hp -= sword * 3
knight_hp -= boss_power
print(boss_hp)
print(knight_hp)

print("Round 6")
boss_hp -= sword * 2 + 4
print(boss_hp)

print("--- summary ---")
print(knight_hp)
print(sword)
# overkill: how far below zero the boss went
print(-boss_hp)
