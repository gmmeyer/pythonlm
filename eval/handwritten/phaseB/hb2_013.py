a = 2
b = 7
c = 6
d = 9
e = 5
f = 1
g = 4
h = 3
i = 8
for t in range(2):
    s = a + b + c
    ok = d + e + f == s and g + h + i == s
    ok = ok and a + d + g == s and b + e + h == s and c + f + i == s
    ok = ok and a + e + i == s and c + e + g == s
    print(ok)
    a, c = c, a
