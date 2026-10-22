target = 64
lo = 0
hi = 99
found = -1
while lo <= hi:
    mid = (lo + hi) // 2
    value = 2 * mid
    if value == target:
        found = mid
        break
    elif value < target:
        lo = mid + 1
    else:
        hi = mid - 1
print(found)
print(lo)
