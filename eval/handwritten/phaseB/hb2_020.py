n = 12
k = 0
while n > 1 and k < 10:
    s = 0
    for d in range(1, n // 2 + 1):
        if n % d == 0:
            s += d
    print(s)
    n = s
    k += 1
print(k)
