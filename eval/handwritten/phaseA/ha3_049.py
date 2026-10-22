print("== start ==")
a = b = c = 4
a -= 9
b *= -b
c //= -3
print(a)
print(b)
print(c)
a, b, c = b, c, a
print(a)
print(b)
print(c)
print()
d = a * c // b
print(d)
e = -d % 7 - -(d % 7)
print(e)
f = e * e * e
print(f)
f -= 999
print(f)
f //= -e
print(f)
f %= d
print(f)
print("f is 'negative'")
g = h = f
g += 1
h -= 1
g, h = h, g
print(g)
print(h)
print(g * h)
print(g * h // -e)
print(-(g * h) % e)
print("tab\there")
print("== end ==")
