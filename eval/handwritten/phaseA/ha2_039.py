a, b = -123, 456
a += b
b = a - b
a -= b
print(a)
print(b)
a, b = a - b, a + b
print(a)
a, b = (a + b) // 2, (b - a) // 2
print(a)
print(b)
