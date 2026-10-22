n = 37
bits = ""
while n > 0:
    bits = str(n % 2) + bits
    n = n // 2
print(bits, len(bits))
print(bits == "100101", bits != "101001")
i = 0
while i < len(bits):
    print(i, bits[i], bits[-1 - i], sep=":", end=" ")
    i += 1
print()
