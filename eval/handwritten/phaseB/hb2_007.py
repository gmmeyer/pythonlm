a0 = 5
d = 7
t = 383
lo = 0
hi = 99
f = -1
while lo <= hi:
    m = (lo + hi) // 2
    v = a0 + d * m
    if v == t:
        f = m
        break
    elif v < t:
        lo = m + 1
    else:
        hi = m - 1
print(f)
print(a0 + d * f == t)
