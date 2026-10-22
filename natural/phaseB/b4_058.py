a = 31
b = 12
c = 25
if a > b:
    a, b = b, a
if b > c:
    b, c = c, b
if a > b:
    a, b = b, a
print(a)
print(b)
print(c)
