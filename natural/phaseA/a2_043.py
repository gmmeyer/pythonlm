# a garden with a path around it
garden_w = 20
garden_h = 12
path = 2
outer = (garden_w + 2 * path) * (garden_h + 2 * path)
inner = garden_w * garden_h
print("outer:")
print(outer)
print("inner:")
print(inner)
print("path area:")
print(outer - inner)
