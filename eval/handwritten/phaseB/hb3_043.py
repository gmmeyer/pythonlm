a = -7
lo = a // 3
hi = a % 3
n = 0
for i in range(lo, hi):
    n += 1
print(n)
for i in range(hi, lo):
    n += 100
print(n)
for i in range(hi, lo, -1):
    n += i
print(n)
print(i)
