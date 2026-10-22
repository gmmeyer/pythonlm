c = 0
for n in range(365, 373):
    a = n // 100
    b = n // 10 % 10
    d = n % 10
    if a * a * a + b * b * b + d * d * d == n:
        print(n)
        c += 1
print(c)
