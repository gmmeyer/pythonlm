n = 998
s = n // 100 + n // 10 % 10 + n % 10
print(s)
s = s // 10 + s % 10
print(s)
s = s // 10 + s % 10
print(s)
print(1 + (n - 1) % 9)
