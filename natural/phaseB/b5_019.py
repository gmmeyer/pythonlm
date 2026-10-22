# 100 in binary, lowest bit first
n = 100
bits = 0
while n != 0:
    print(n % 2)
    n //= 2
    bits += 1
print("that was 100 written backwards")
print(bits)
