# first number with exactly six divisors
n = 1
while True:
    count = 0
    for d in range(1, n + 1):
        if n % d == 0:
            count += 1
    if count == 6:
        break
    n += 1
print(n)
