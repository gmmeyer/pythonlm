# largest gap between neighbouring multiples of 7 or 11 up to 60
prev = 0
best = 0
for n in range(1, 61):
    if n % 7 == 0 or n % 11 == 0:
        if n - prev > best:
            best = n - prev
        prev = n
print(best)
print(prev)
