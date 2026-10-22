# 3^13 mod 17 by repeated squaring
base = 3
exp = 13
mod = 17
result = 1
while exp > 0:
    if exp % 2 == 1:
        result = result * base % mod
    base = base * base % mod
    exp //= 2
print(result)
