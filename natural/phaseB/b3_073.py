# running max and min of a wobbling sequence
x = 7
hi = x
lo = x
for i in range(12):
    x = (x * 5 + 3) % 23
    print(x)
    if x > hi:
        hi = x
    if x < lo:
        lo = x
print(hi)
print(lo)
