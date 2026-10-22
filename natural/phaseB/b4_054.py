# first number above 100 divisible by both 7 and 11
n = 101
while True:
    if n % 7 == 0 and n % 11 == 0:
        break
    n += 1
print(n)
