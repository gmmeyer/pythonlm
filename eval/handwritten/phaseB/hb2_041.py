c = 0
for n in range(123, 148):
    a = n // 100
    b = n // 10 % 10
    d = n % 10
    if not a < b < d:
        continue
    c += 1
print(c)
