# which of these are abundant?
for n in range(12, 25, 4):
    s = 0
    for d in range(1, n // 2 + 1):
        if n % d == 0:
            s += d
    if s > n:
        print(n)
