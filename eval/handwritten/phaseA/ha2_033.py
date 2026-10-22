a, b, c = 1, 2, 3
a, b, c = b, c, a
print(a * 100 + b * 10 + c)
a, b, c = b, c, a
print(a * 100 + b * 10 + c)
a, b, c = c, a, b
a, b = b, a
print(a * 100 + b * 10 + c)
