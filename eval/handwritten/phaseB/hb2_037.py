t = 500
lo = 0
hi = 30
while lo < hi:
    m = (lo + hi) // 2
    if m * m + m < t:
        lo = m + 1
    else:
        hi = m
print(lo)
print(lo * lo + lo)
print((lo - 1) * (lo - 1) + lo - 1 < t <= lo * lo + lo)
