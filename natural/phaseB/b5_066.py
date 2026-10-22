# is 19 a happy number? square the digits until we hit 1 or loop
n = 19
seen_steps = 0
while n != 1 and seen_steps < 20:
    s = 0
    while n > 0:
        d = n % 10
        s += d * d
        n //= 10
    n = s
    seen_steps += 1
print(n == 1)
print(seen_steps)
