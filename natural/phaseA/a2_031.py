# swap the hundreds digit and the ones digit
n = 214
h = n // 100
t = n // 10 % 10
o = n % 10
h, o = o, h
print(h * 100 + t * 10 + o)
