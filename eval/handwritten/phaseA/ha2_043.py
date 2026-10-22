c = 87
q = c // 25
c %= 25
d = c // 10
c %= 10
n = c // 5
c %= 5
print(q)
print(d)
print(n)
print(c)
print(q * 25 + d * 10 + n * 5 + c)
