# which b in 1..13 makes gcd(13, b) take the most steps?
best = 0
best_b = 0
for b in range(1, 14):
    x = 13
    y = b
    steps = 0
    while y != 0:
        x, y = y, x % y
        steps += 1
    if steps > best:
        best = steps
        best_b = b
print(best_b)
print(best)
