# powers of two among 1..40, printed as they turn up
for n in range(1, 41):
    m = n
    while m > 1 and m % 2 == 0:
        m = m // 2
    if m == 1:
        print(n)
