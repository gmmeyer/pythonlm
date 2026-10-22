r = 7
y = r
c = 0
for x in range(0, r + 1):
    while x * x + y * y > r * r:
        y -= 1
    if x == 0:
        c += 2 * y + 1
    else:
        c += 2 * (2 * y + 1)
print(c)
