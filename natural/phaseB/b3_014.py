# first n where the square ends in 21
n = 1
while n * n % 100 != 21:
    n += 1
print(n)
print(n * n)
