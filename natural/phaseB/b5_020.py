# binary digits of 600, counting how many are ones
n = 600
ones = 0
total_bits = 0
while n > 0:
    ones += n % 2
    total_bits += 1
    n //= 2
print(total_bits)
print(ones)
