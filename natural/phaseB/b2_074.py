# population: two species, one grows while the other shrinks
rabbits = 10
foxes = 40
year = 0
while foxes > rabbits:
    year += 1
    rabbits += rabbits // 2 + 1
    foxes -= 5
print(year)
print(rabbits)
print(foxes)
