n = 4
t = 1
for _ in range(n):
    t *= 2
c = 0
for m in range(1, t):
    k = m
    d = 1
    while k % 2 == 0:
        k //= 2
        d += 1
    if d == 1:
        c += 1
    print(d)
print(c)
