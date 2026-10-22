# lower member of each twin prime pair below 32
prev = 2
for n in range(3, 32):
    is_prime = True
    d = 2
    while d * d <= n:
        if n % d == 0:
            is_prime = False
            break
        d += 1
    if is_prime:
        if n - prev == 2:
            print(prev)
        prev = n
