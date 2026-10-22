g1 = 713
g2 = 398
g3 = 927
g4 = 79
t = 0
p = 0
for k in range(4):
    if k == 0:
        x = g1
    elif k == 1:
        x = g2
    elif k == 2:
        x = g3
    else:
        x = g4
    for _ in range(3):
        d = x % 10
        x //= 10
        if p % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        t += d
        p += 1
print(t)
print(t % 10 == 0)
