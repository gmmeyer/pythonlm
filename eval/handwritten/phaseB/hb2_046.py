x = 1
y = 1
while x <= 31:
    print(x * x - 2 * y * y)
    x, y = x + 2 * y, x + y
print(x)
print(y)
