# the 7th prime
count = 0
n = 1
while count < 7:
    n += 1
    is_prime = True
    for d in range(2, n):
        if d * d > n:
            break
        if n % d == 0:
            is_prime = False
            break
    if is_prime:
        count += 1
print(n)
