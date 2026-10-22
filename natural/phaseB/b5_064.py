# is 28 a perfect number? add up its proper divisors
n = 28
total = 0
for d in range(1, n):
    if n % d == 0:
        total += d
print(total)
print(total == n)
