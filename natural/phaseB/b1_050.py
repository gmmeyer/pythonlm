# Goldbach: smallest prime p with 30 - p also prime
n = 30
p = 2
while p <= n // 2:
    q = n - p
    p_ok = True
    q_ok = True
    d = 2
    while d * d <= q:
        if p % d == 0 and d < p:
            p_ok = False
        if q % d == 0:
            q_ok = False
        d += 1
    if p_ok and q_ok:
        print(p)
        print(q)
        break
    p += 1
