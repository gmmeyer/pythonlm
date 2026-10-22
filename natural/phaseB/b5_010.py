# is 64 a power of two? keep halving while it is even
n = 64
while n > 1 and n % 2 == 0:
    n = n // 2
print(n == 1)
