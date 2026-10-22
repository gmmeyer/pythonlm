n = 7
steps = 0
while n != 1 and steps < 40:
    if n % 2 == 0:
        n //= 2
    else:
        n = 3 * n + 1
    steps += 1
print(steps)
print(n)
