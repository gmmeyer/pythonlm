# integer square root of 987 by binary search
n = 987
lo = 0
hi = 40
while lo < hi:
    mid = (lo + hi + 1) // 2
    if mid * mid <= n:
        lo = mid
    else:
        hi = mid - 1
print(lo)
print(lo * lo <= n < (lo + 1) * (lo + 1))
