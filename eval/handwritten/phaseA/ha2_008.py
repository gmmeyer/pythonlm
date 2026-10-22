a = b = c = 3
a += 4
b *= a
c, a = a - c, c + b
b, c = c, b
a -= b * c
print(a)
print(b)
print(c)
