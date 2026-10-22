n = 53
bits = ""
while n > 0:
    bits = str(n % 2) + bits
    n //= 2
print("53 in binary is", bits)
