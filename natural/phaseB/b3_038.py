# first n > 10 whose square ends in 56
n = 11
while True:
    if n * n % 100 == 56:
        print(n)
        print(n * n)
        break
    n += 1
