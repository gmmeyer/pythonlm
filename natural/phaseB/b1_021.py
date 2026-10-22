# happy number test for 19
n = 19
steps = 0
while n != 1 and steps < 10:
    s = 0
    while n > 0:
        d = n % 10
        s += d * d
        n //= 10
    n = s
    steps += 1
print(steps)
