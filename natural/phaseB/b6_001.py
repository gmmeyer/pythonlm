# parcels of 1..12 kg, flat shipping tiers
total = 0
expensive = 0
for w in range(1, 13):
    if w <= 3:
        cost = 4
    elif w <= 8:
        cost = 8
    else:
        cost = 12
    total += cost
    if cost > 10:
        expensive += 1
print(total)
print(expensive)
