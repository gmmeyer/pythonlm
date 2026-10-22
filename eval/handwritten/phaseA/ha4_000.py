# A duel in the dungeon, played out round by round.
# The hero and the goblin trade blows. There are no loops yet,
# so every round is written out by hand.

hero_hp = 60
goblin_hp = 45
hero_attack = 9
goblin_attack = 7
potions = 2

print("Round 1")
goblin_hp -= hero_attack
hero_hp -= goblin_attack
print(hero_hp)
print(goblin_hp)

print("Round 2")
# the hero lands a critical hit: double damage
goblin_hp -= hero_attack * 2
hero_hp -= goblin_attack
print(hero_hp)
print(goblin_hp)

print("Round 3")
# the goblin gets angry: its attack grows by a third
goblin_attack += goblin_attack // 3
hero_hp -= goblin_attack
goblin_hp -= hero_attack
print(hero_hp)
print(goblin_hp)

print("Round 4")
# the hero drinks a potion that heals 15, then takes another hit
potions -= 1
hero_hp += 15
hero_hp -= goblin_attack
print(hero_hp)
print(potions)

print("Round 5")
goblin_hp -= hero_attack
print(goblin_hp)

print("--- summary ---")
damage_taken = 60 - hero_hp
print(damage_taken)
print(potions)
