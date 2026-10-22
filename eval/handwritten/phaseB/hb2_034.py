k = 6
n = 1
while True:
    c = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            c += 2
            if d * d == n:
                c -= 1
        d += 1
    if c == k:
        break
    n += 1
print(n)
