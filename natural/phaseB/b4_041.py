n = 7
steps = 0
highest = n
while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    if n > highest:
        highest = n
    steps += 1
print(steps)
print(highest)
