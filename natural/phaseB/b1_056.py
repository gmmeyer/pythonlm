# Mersenne numbers that are prime
m = 1
for p in range(2, 10):
    m = 2 * m + 1
    is_prime = True
    d = 2
    while d * d <= m:
        if m % d == 0:
            is_prime = False
            break
        d += 1
    if is_prime:
        print(m)
