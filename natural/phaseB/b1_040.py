# Armstrong numbers between 150 and 159
for n in range(150, 160):
    m = n
    total = 0
    while m > 0:
        d = m % 10
        total += d * d * d
        m //= 10
    if total == n:
        print(n)
