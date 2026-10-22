# A hero earns experience points (XP) on quests.
# Every 100 XP is a new level; leftover XP carries over.
# A monster gives 15 XP per monster level, plus 5.

level = 1
xp = 0

print("Quest 1: slime")
monster = 2
xp += monster * 15 + 5
level += xp // 100
xp %= 100
print(level)
print(xp)

print("Quest 2: wolf")
monster = 4
xp += monster * 15 + 5
level += xp // 100
xp %= 100
print(level)
print(xp)

print("Quest 3: troll")
monster = 7
xp += monster * 15 + 5
level += xp // 100
xp %= 100
print(level)
print(xp)

print("Quest 4: dragon")
monster = 20
xp += monster * 15 + 5
level += xp // 100
xp %= 100
print(level)
print(xp)

print("Knocked out!")
# the hero loses a level and half of the spare XP
level -= 1
xp -= xp // 2
print(level)
print(xp)

print("Quest 5: double XP weekend")
monster = 9
xp += (monster * 15 + 5) * 2
level += xp // 100
xp %= 100
print(level)
print(xp)

print("--- hero ---")
print((level - 1) * 100 + xp)
