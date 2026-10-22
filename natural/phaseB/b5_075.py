# elevator ping-pongs between floors 1 and 6
floor = 1
direction = 1
visits = 0
for tick in range(20):
    floor += direction
    if floor == 6 or floor == 1:
        direction = -direction
    if floor == 1:
        visits += 1
print(floor)
print(direction)
print(visits)
