# the sorted values are 2*i for i in 0..99, so odd targets are missing
target = 51
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
