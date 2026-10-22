n = 1
k = 0
while n <= 100:
    s = 0
    m = n
    while m > 0:
        s += m % 10
        m //= 10
    n += s
    k += 1
print(n)
print(k)
