# modular inverse of 7 mod 26
inv = 0
for x in range(1, 26):
    if 7 * x % 26 == 1:
        inv = x
        break
print(inv)
