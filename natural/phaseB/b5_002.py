# smallest x with x * x >= 500, found by bisection
lo = 0
hi = 50
while lo < hi:
    mid = (lo + hi) // 2
    if mid * mid >= 500:
        hi = mid
    else:
        lo = mid + 1
print(lo)
print(lo * lo)
