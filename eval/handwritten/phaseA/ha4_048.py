# A post office counter weighs parcels in grams.
# Postage is 4 coins plus 3 coins for every started 250 grams.
# The day's weight is added up in tens of grams to keep numbers small.

postage = 0
weight = 0
parcels = 0

print("Parcel: 120 g")
w = 120
cost = 4 + (w + 249) // 250 * 3
postage += cost
weight += w // 10
parcels += 1
print(cost)

print("Parcel: 480 g")
w = 480
cost = 4 + (w + 249) // 250 * 3
postage += cost
weight += w // 10
parcels += 1
print(cost)

print("Parcel: 731 g")
w = 731
cost = 4 + (w + 249) // 250 * 3
postage += cost
weight += w // 10
parcels += 1
print(cost)

print("Parcel: 250 g")
w = 250
cost = 4 + (w + 249) // 250 * 3
postage += cost
weight += w // 10
parcels += 1
print(cost)

print("Parcel: 600 g")
w = 600
cost = 4 + (w + 249) // 250 * 3
postage += cost
weight += w // 10
parcels += 1
print(cost)

print("--- day ---")
print(parcels)
print(postage)
# kilograms, then the rest in grams
print(weight // 100)
print(weight % 100 * 10)
print(postage // parcels)
print(postage % parcels)
