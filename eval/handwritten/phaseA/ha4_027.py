# Miners dig ore over four shifts. The cart carries 60 kg up the shaft,
# every trip burns 3 coins of lamp oil, and ore sells at 1 coin per 4 kg.

stock = 0
coins = 50
cart = 60
trips_total = 0

print("Shift 1")
dug = 145
trips = (dug + cart - 1) // cart
stock += dug
coins -= trips * 3
trips_total += trips
print(trips)
print(coins)

print("Shift 2")
dug = 222
trips = (dug + cart - 1) // cart
stock += dug
coins -= trips * 3
trips_total += trips
print(trips)
print(coins)

print("Market day")
coins += stock // 4
stock %= 4
print(coins)
print(stock)

print("Shift 3")
dug = 98
trips = (dug + cart - 1) // cart
stock += dug
coins -= trips * 3
trips_total += trips
print(trips)
print(coins)

print("Shift 4: cave-in")
# a third of the ore is buried again
dug = 180
dug -= dug // 3
trips = (dug + cart - 1) // cart
stock += dug
coins -= trips * 3
trips_total += trips
print(trips)
print(coins)

print("--- season ---")
coins += stock // 4
stock %= 4
print(coins)
print(stock)
print(trips_total)
