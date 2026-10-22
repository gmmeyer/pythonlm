n = 700
lo = 0
hi = 31
while lo < hi:
    m = (lo + hi + 1) // 2
    if m * m <= n:
        lo = m
    else:
        hi = m - 1
print(lo)
print(lo * lo <= n < (lo + 1) * (lo + 1))
