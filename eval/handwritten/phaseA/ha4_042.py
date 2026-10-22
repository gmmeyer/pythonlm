# A snail at the bottom of a 2 meter well (200 cm).
# By day it climbs 47 cm; by night it slips back 25 cm,
# or 40 cm on rainy nights. We follow it until it gets out.

height = 0
up = 47
slip = 25
slipped = 0

print("Day 1")
height += up - slip
slipped += slip
print(height)

print("Day 2")
height += up - slip
slipped += slip
print(height)

print("Day 3: rainy night")
slip = 40
height += up - slip
slipped += slip
slip = 25
print(height)

print("Day 4")
height += up - slip
slipped += slip
print(height)

print("Day 5")
height += up - slip
slipped += slip
print(height)

print("Day 6")
height += up - slip
slipped += slip
print(height)

print("Day 7: rainy night")
slip = 40
height += up - slip
slipped += slip
slip = 25
print(height)

print("Day 8")
height += up - slip
slipped += slip
print(height)

print("Day 9")
height += up - slip
slipped += slip
print(height)

print("Day 10: out by evening")
height += up
print(height)

print("--- the snail ---")
print(height - 200)
print(slipped)
print(up * 10 - slipped)
