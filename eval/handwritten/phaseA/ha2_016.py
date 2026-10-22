k, b = 5, 8
x = 19
y = (k * x + b) % 26
print(y)
print(21 * (y - b) % 26)
x = 25
y = (k * x + b) % 26
print(y)
print(21 * (y - b) % 26)
print(k * 21 % 26)
