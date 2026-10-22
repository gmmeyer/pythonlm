# A three-level parking garage with 40 spaces per level.
# Cars fill level 1 first, then 2, then 3.
# Parking costs 2 coins per hour, paid when a car leaves.

per_level = 40
parked = 0
earnings = 0
fee = 2

print("8 am")
parked += 37
print(parked // per_level)
print(parked % per_level)

print("10 am")
parked += 58
print(parked // per_level)
print(parked % per_level)
print(3 * per_level - parked)

print("1 pm: lunch")
# 22 cars leave after 5 hours
leaving = 22
earnings += leaving * 5 * fee
parked -= leaving
print(parked)
print(earnings)

print("3 pm")
parked += 41
print(parked // per_level)
print(parked % per_level)
print(3 * per_level - parked)

print("6 pm: closing")
# 60 cars stayed 4 hours, the rest 2 hours
leaving = 60
earnings += leaving * 4 * fee
parked -= leaving
earnings += parked * 2 * fee
parked = 0
print(earnings)

print("--- day ---")
print(earnings // 100)
print(earnings % 100)
print(parked)
