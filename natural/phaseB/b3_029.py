# count primes below 30
count = 0
for n in range(2, 30):
    prime = True
    for d in range(2, n):
        if d * d > n:
            break
        if n % d == 0:
            prime = False
            break
    if prime:
        count += 1
print(count)
