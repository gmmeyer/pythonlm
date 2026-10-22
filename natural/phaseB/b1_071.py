n = 7
peak = n
steps = 0
while n != 1:
    if n % 2 == 0:
        n //= 2
    else:
        n = 3 * n + 1
    if n > peak:
        peak = n
    steps += 1
print(steps)
print(peak)
