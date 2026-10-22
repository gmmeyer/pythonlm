# painting the bedroom
wall_w = 12
wall_h = 9
walls = 4
door = 21
window = 15
area = wall_w * wall_h * walls - door - window * 2
print(area)
per_can = 40
cans = (area + per_can - 1) // per_can
print(cans)
coats = 2
print(cans * coats)
