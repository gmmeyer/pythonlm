for p in range(5, 14, 2):
    f = 1
    for i in range(2, p):
        f = f * i % p
    print(f == p - 1)
