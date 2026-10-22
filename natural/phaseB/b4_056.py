lo = 999
hi = -999
for i in range(12):
    v = (i - 5) * (i - 5) - 10
    if v < lo:
        lo = v
    elif v > hi:
        hi = v
print(lo)
print(hi)
