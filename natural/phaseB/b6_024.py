# elevator goes up to floor 9, then back down, stopping at floors 3, 6 and 9
floor = 0
stops = 0
direction = 1
for step in range(24):
    floor += direction
    if floor == 9:
        direction = -1
    elif floor == 0:
        direction = 1
    if floor % 3 == 0:
        stops += 1
print(floor)
print(stops)
