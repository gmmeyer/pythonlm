# A farmer's storehouse, season by season.
# The family eats wheat every season, a quarter of the store is sown in spring,
# and spare wheat is sold in autumn in sacks of 25 for 4 coins a sack.

wheat = 120
coins = 30
family = 5
eat_per_person = 8

print("Spring")
wheat -= family * eat_per_person
seed = wheat // 4
wheat -= seed
print(wheat)
print(seed)

print("Summer")
# a good harvest: every sown unit gives back 9
harvest = seed * 9
wheat += harvest
wheat -= family * eat_per_person
print(harvest)
print(wheat)

print("Autumn")
harvest = seed * 6
wheat += harvest
wheat -= family * eat_per_person
# keep 100 for winter, sell whole sacks of the rest
sacks = (wheat - 100) // 25
wheat -= sacks * 25
coins += sacks * 4
print(sacks)
print(wheat)
print(coins)

print("Winter")
# a baby is born, so one more mouth to feed
family += 1
wheat -= family * eat_per_person
coins -= 12
print(wheat)
print(coins)

print("--- next spring ---")
# buy back wheat at 1 coin for every 3
bought = coins // 2 * 3
coins -= coins // 2
wheat += bought
print(wheat)
print(coins)
