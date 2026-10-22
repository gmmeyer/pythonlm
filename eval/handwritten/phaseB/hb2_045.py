N = 43
a0 = 0
while (a0 + 1) * (a0 + 1) <= N:
    a0 += 1
m = 0
d = 1
a = a0
k = 0
while a != 2 * a0:
    m = d * a - m
    d = (N - m * m) // d
    a = (a0 + m) // d
    print(a)
    k += 1
print(k)
