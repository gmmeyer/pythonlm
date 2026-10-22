n = 987
s = n % 10
n //= 10
s += n % 10
n //= 10
s += n % 10
n //= 10
print(s)
r = s % 9
print(r)
t = s // 10 + s % 10
print(t)
print(n)
