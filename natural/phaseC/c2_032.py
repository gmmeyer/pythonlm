number = 173
n = number
bits = ""
while n > 0:
    bits = str(n % 2) + bits
    n //= 2
print(number, "in binary is", bits)
