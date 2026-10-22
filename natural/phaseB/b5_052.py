# validate a, b, c shifting from negative to positive
bad = 0
for t in range(-2, 3):
    a = t
    b = t + 1
    c = t + 2
    if not (a > 0 and b > 0 and c > 0):
        bad += 1
print(bad)
