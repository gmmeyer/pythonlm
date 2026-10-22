n = 28
s = 0
for d in range(1, n):
    if n % d != 0:
        continue
    s += d
print(s)
print(s == n)
