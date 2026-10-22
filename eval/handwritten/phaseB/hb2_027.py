for n in range(37, 130, 92):
    x = n
    r = 0
    for _ in range(8):
        r = r * 2 + x % 2
        x //= 2
    print(r)
    print(r == n)
