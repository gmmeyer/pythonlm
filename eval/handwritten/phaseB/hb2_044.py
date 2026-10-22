p = 4
q = 13
while p > 0:
    if q % p == 0:
        print(q // p)
        break
    c = q // p + 1
    print(c)
    p = p * c - q
    q = q * c
    x = p
    y = q
    while y:
        x, y = y, x % y
    p //= x
    q //= x
