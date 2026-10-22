count = 0
n = 2
while n < 20:
    d = 2
    is_prime = True
    while d * d <= n and is_prime:
        if n % d == 0:
            is_prime = False
        d += 1
    if is_prime:
        count += 1
    n += 1
print(count)
