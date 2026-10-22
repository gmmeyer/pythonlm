# trailing zero bits of 88 (binary 1011000)
n = 88
zeros = 0
while n % 2 == 0:
    n = n // 2
    zeros += 1
print(zeros)
print(n)
