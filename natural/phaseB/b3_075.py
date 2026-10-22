# longest run of numbers below 30 whose digit sum is under 6
best = 0
run = 0
for n in range(1, 30):
    if n // 10 + n % 10 < 6:
        run += 1
        if run > best:
            best = run
    else:
        run = 0
print(best)
