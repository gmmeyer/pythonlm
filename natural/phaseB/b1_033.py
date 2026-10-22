# multiplicative persistence of 39
n = 39
steps = 0
while n >= 10:
    p = 1
    while n > 0:
        p *= n % 10
        n //= 10
    n = p
    steps += 1
print(steps)
