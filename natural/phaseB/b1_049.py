# divisibility by 11 with an alternating digit sum
n = 429
sign = 1
alt = 0
while n > 0:
    alt += sign * (n % 10)
    sign = -sign
    n //= 10
print(alt)
print(alt % 11 == 0)
