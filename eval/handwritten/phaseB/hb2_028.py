for n in range(10, 14):
    a = n
    b = n // 2
    g = 0
    p = 1
    while a > 0:
        if a % 2 != b % 2:
            g += p
        a //= 2
        b //= 2
        p *= 2
    print(g)
