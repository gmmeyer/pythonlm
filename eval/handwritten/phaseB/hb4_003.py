# Predator and prey with integer rules. Rabbits breed by a quarter each
# season, a few migrate in, and every fox eats two. Foxes grow when they
# ate well and starve otherwise. Both populations are capped.
rabbits = 40
foxes = 6
season = 0
print("rabbits and foxes")
while season < 10:
    season += 1
    births = rabbits // 4
    eaten = foxes * 2
    if eaten > rabbits:
        eaten = rabbits
    rabbits = rabbits + births - eaten + 4
    if rabbits > 200:
        rabbits = 200
    if eaten >= foxes * 2 and rabbits > 20:
        foxes += foxes // 3 + 1
    else:
        foxes -= foxes // 2
    if foxes > 40:
        foxes = 40
    if foxes < 1:
        foxes = 1
    print("season")
    print(season)
    print(rabbits)
    print(foxes)
print("more rabbits than three per fox")
print(rabbits > foxes * 3)
