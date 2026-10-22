a = 37
b = 23
p = 0
while a > 0:
    if a % 2 == 1:
        p += b
    a //= 2
    if a > 0:
        b *= 2
print(p)
print(p == 37 * 23)
