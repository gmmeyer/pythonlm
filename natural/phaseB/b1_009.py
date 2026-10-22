# Armstrong check
n = 153
m = n
total = 0
while m > 0:
    d = m % 10
    total += d * d * d
    m //= 10
print(total == n)
