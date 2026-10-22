n = 100
for p in range(2, 8):
    if p == 4 or p == 6:
        continue
    e = 0
    q = n
    while q >= p:
        q //= p
        e += q
    print(e)
