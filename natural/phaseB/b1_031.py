# amicable pair 220 and 284
n = 220
s = 1
d = 2
while d * d <= n:
    if n % d == 0:
        s += d
        if d * d != n:
            s += n // d
    d += 1
print(s)
n = s
t = 1
d = 2
while d * d <= n:
    if n % d == 0:
        t += d
        if d * d != n:
            t += n // d
    d += 1
print(t)
print(t == 220)
