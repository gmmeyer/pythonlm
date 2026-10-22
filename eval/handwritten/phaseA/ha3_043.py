a = 5
b = 3
a, b = a + b, a - b
print(a)
print(b)
a, b = a + b, a - b
print(a)
print(b)
a, b = (a + b) // 2, (a - b) // 2
print(a)
print(b)
a, b = b - a, a * b
print(a)
print(b)
a, b = b % a, b // a
print(a)
print(b)
