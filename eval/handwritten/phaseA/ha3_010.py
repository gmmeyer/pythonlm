a = 1
b = 2
c = 3
a, b, c = c, a, b
print(a)
print(b)
print(c)
a, b, c = c, a, b
print(a * 100 + b * 10 + c)
a, b, c = c, a, b
print(a * 100 + b * 10 + c)
a, b, c = b, c, a
print(a * 100 + b * 10 + c)
