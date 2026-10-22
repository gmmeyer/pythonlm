# trailing decimal zeros of 600, and of 12000 // 10
n = 600
zeros = 0
while n % 10 == 0:
    n //= 10
    zeros += 1
print(zeros)
print(n)
