# largest n below 100 divisible by 7 whose digit sum is even
n = 99
while n > 0:
    if n % 7 == 0 and (n // 10 + n % 10) % 2 == 0:
        break
    n -= 1
print(n)
