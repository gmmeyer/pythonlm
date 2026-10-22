x = 0
y = 4
print((x or y) == 4)
print((x and y) == 0)
print((y and x) < (x or y))
z = (y or x) * 2 + (x and y)
print(z)
