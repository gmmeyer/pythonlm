# A rooftop water tank holds at most 400 liters.
# Rain fills it and the household drains it. Anything above 400 spills:
#   spill = level // 400 * (level % 400)
# (the trick only works while the level stays below 800).

level = 150
spilled = 0
used = 0

print("Day 1: storm")
level += 310
spill = level // 400 * (level % 400)
level -= spill
spilled += spill
print(level)
print(spill)

print("Day 2: dry")
level -= 95
used += 95
print(level)

print("Day 3: rain")
level += 220
spill = level // 400 * (level % 400)
level -= spill
spilled += spill
print(level)
print(spill)

print("Day 4: laundry")
level -= 180
used += 180
print(level)

print("Day 5: drizzle")
level += 179
spill = level // 400 * (level % 400)
level -= spill
spilled += spill
print(level)
print(spill)

print("Day 6: one more liter")
level += 1
spill = level // 400 * (level % 400)
level -= spill
spilled += spill
print(level)
print(spill)

print("Day 7: garden")
# the garden takes a third of whatever is in the tank
used += level // 3
level -= level // 3
print(level)

print("--- week ---")
print(spilled)
print(used)
