n = 217
ones = 0
while n > 0:
    ones += n % 2
    n //= 2
print(ones)
