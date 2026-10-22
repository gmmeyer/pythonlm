# inventory with two warehouses
north = 25
south = 5
moved = 0
while south < 15 and north > 10:
    north -= 3
    south += 3
    moved += 3
print(north)
print(south)
print(moved)
