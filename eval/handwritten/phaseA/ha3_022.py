n = -742
print(n // 100)
print(n // 10 % 10)
print(n % 10)
m = -n
print(m // 100)
print(m // 10 % 10)
print(m % 10)
print(-(m % 10))
r = (m % 10) * 100 + (m // 10 % 10) * 10 + m // 100
print(r)
print(r - m)
