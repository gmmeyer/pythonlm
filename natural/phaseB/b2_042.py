# elevator going up and down between floors 1 and 6
floor = 1
going_up = True
trips = 0
for tick in range(20):
    if going_up:
        floor += 1
        if floor == 6:
            going_up = False
    else:
        floor -= 1
        if floor == 1:
            going_up = True
            trips += 1
print(floor)
print(going_up)
print(trips)
