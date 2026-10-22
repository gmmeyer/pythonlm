# primes below 30 by trial division
for n in range(2, 30):
    is_prime = True
    d = 2
    while d * d <= n:
        if n % d == 0:
            is_prime = False
            break
        d += 1
    if is_prime:
        print(n)
