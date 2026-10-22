c = 0
for n in range(16, 25, 2):
    s = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            s += d
            if d * d != n:
                s += n // d
        d += 1
    if s > n:
        c += 1
        print(n)
print(c)
