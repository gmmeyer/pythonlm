total = 0
found = 0
n = 2
while found < 8:
    is_prime = True
    d = 2
    while d * d <= n:
        if n % d == 0:
            is_prime = False
            break
        d += 1
    if is_prime:
        total += n
        found += 1
    n += 1
print(total)
