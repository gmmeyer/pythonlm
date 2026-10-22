c = 0
last = 0
for n in range(100, 125):
    s = n // 100 + n // 10 % 10 + n % 10
    if n % s == 0:
        c += 1
        last = n
print(c)
print(last)
