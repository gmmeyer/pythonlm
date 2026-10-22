n = 846
k = 0
while n > 0:
    d = n % 10
    print("10^" + str(k), "|" + "=" * d, d)
    n //= 10
    k += 1
