# marathon: water every 5 km, a cheering crowd every 8 km
water = 0
crowds = 0
both = 0
for km in range(1, 43):
    w = km % 5 == 0
    c = km % 8 == 0
    if w:
        water += 1
    if c:
        crowds += 1
    if w and c:
        both += 1
print(water)
print(crowds)
print(both)
