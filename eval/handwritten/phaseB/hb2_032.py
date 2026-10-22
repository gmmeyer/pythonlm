for p in range(21, 32, 2):
    b = 2
    e = p - 1
    r = 1
    while e > 0:
        if e % 2 == 1:
            r = r * b % p
        b = b * b % p
        e //= 2
    print(r == 1)
