# water the garden when it's been 3 dry days; rain counts as watering
last_watered = 0
waterings = 0
for day in range(1, 15):
    rained = day % 5 == 0
    if rained:
        last_watered = day
        continue
    if day - last_watered >= 3:
        print(day)
        waterings += 1
        last_watered = day
print(waterings)
