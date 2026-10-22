# first abundant number
n = 2
while True:
    s = 0
    for d in range(1, n):
        if n % d == 0:
            s += d
    if s > n:
        break
    n += 1
print(n)
