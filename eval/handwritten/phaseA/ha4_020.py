# A koi pond over five days. Each fish eats 4 pellets a day,
# and the keeper buys 30 more pellets every evening.
# A heron visits on day 3, and on day 4 the food runs short.

fish = 23
pellets = 200
thin = 0

print("Day 1")
pellets -= fish * 4
pellets += 30
print(pellets)

print("Day 2")
pellets -= fish * 4
pellets += 30
print(pellets)

print("Day 3: heron")
# the heron takes a fifth of the fish
fish -= fish // 5
pellets -= fish * 4
pellets += 30
print(fish)
print(pellets)

print("Day 4: short of food")
fed = pellets // 4
thin = fish - fed
pellets %= 4
# a big sack arrives in the evening
pellets += 400
print(fed)
print(thin)
print(pellets)

print("Day 5: eggs hatch")
# every well-fed fish adds two babies
fish += fed * 2
pellets -= fish * 4
print(fish)
print(pellets)

print("--- pond ---")
# how many more full days the pellets last
print(pellets // (fish * 4))
print(pellets % (fish * 4))
