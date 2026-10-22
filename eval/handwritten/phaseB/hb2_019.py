c = 0
for n in range(121, 900, 77):
    r = 0
    m = n
    while m > 0:
        r = r * 10 + m % 10
        m //= 10
    if r == n:
        print(n)
        c += 1
print(c)
