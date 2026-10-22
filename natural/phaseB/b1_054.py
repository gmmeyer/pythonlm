# trailing zeros of 100!
n = 100
zeros = 0
p = 5
while p <= n:
    zeros += n // p
    p *= 5
print(zeros)
