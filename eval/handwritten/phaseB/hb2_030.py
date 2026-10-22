n = 999
x = n
y = x // 2 + 1
while y < x:
    x = y
    y = (x + n // x) // 2
print(x)
print(x * x <= n)
print(n - x * x)
