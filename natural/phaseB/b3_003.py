# first number above 100 divisible by both 7 and 13
n = 100
while n % 7 != 0 or n % 13 != 0:
    n += 1
print(n)
