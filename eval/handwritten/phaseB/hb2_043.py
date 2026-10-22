n = 7
a = 0
b = 1
c = 1
d = n
t = 1
while c <= n:
    k = (n + b) // d
    e = k * c - a
    f = k * d - b
    a = c
    b = d
    c = e
    d = f
    t += 1
print(t)
