n = 487
a, b, c = n // 100, n // 10 % 10, n % 10
r = c * 100 + b * 10 + a
print(r)
print(n - r)
print((n - r) // 99)
