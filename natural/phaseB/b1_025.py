n = 97
is_prime = True
for d in range(2, 10):
    if d * d > n:
        break
    if n % d == 0:
        is_prime = False
        break
print(is_prime)
