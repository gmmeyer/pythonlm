# An archery contest: three archers, three arrows each.
# An arrow scores 10 minus (distance from the center // 4), with the
# distance in centimeters. A steady wind pushes every arrow 3 cm further.

wind = 3
anna = 0
bram = 0
cleo = 0

print("Anna")
arrow = 5
anna += 10 - (arrow + wind) // 4
arrow = 1
anna += 10 - (arrow + wind) // 4
arrow = 14
anna += 10 - (arrow + wind) // 4
print(anna)

print("Bram")
arrow = 0
bram += 10 - (arrow + wind) // 4
arrow = 22
bram += 10 - (arrow + wind) // 4
arrow = 9
bram += 10 - (arrow + wind) // 4
print(bram)

print("Cleo")
arrow = 2
cleo += 10 - (arrow + wind) // 4
arrow = 6
cleo += 10 - (arrow + wind) // 4
arrow = 3
cleo += 10 - (arrow + wind) // 4
print(cleo)

print("Wind drops: one bonus arrow each")
wind = 0
arrow = 7
anna += 10 - (arrow + wind) // 4
arrow = 30
bram += 10 - (arrow + wind) // 4
arrow = 4
cleo += 10 - (arrow + wind) // 4

print("--- results ---")
print(anna)
print(bram)
print(cleo)
total = anna + bram + cleo
print(total // 3)
print(total % 3)
