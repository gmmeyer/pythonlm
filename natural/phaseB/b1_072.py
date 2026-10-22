# longest Collatz run for starts below 9
best = 1
best_steps = 0
for start in range(1, 9):
    n = start
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    if steps > best_steps:
        best_steps = steps
        best = start
print(best)
print(best_steps)
