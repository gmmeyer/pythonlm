a = b = c = d = e = 7
a += 1
b += 2
c += 3
d += 4
e += 5
a, b, c = c, a, b
d, e = e, d
print(a)
print(b)
print(c)
print(d)
print(e)
a, b, c = c, b, a
d, e = -e, -d
print(a * 10 + e)
print(b * 10 + d)
print(c)
