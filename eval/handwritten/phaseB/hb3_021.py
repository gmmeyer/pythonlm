a = b = 4
a, b = b + 1, a - 1
print(a)
print(b)
f = g = a > b
print(f)
print(f == g)
a, b = b, a
print(a > b)
