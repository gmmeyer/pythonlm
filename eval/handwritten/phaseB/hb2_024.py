n = 679
p = 0
while n >= 10:
    m = 1
    while n > 0:
        m *= n % 10
        n //= 10
    n = m
    p += 1
    print(n)
print(p)
