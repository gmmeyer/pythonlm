n = 795
a = n % 10
b = n // 10 % 10 * 2
c = n // 100
t = a + b // 10 + b % 10 + c
print(t)
print((10 - t % 10) % 10)
