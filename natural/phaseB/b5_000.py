# binary search for 37 in the implicit sorted range 0..100
target = 37
lo = 0
hi = 100
probes = 0
while lo <= hi:
    mid = (lo + hi) // 2
    probes += 1
    if mid == target:
        break
    elif mid < target:
        lo = mid + 1
    else:
        hi = mid - 1
print(mid)
print(probes)
