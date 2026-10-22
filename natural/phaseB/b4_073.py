n = 77
ones = 0
while n > 0:
    if n % 2 == 1:
        ones += 1
    n = n // 2
print(ones)
