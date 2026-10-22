n = 437
b = 7
p = 1
while p <= n // b:
    p *= b
while p > 0:
    print(n // p)
    n %= p
    p //= b
