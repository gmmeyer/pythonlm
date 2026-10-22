# 345 in base 8, least significant digit first
n = 345
while n > 0:
    print(n % 8)
    n //= 8
