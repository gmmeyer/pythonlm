c = 25
a = 1
b = 24
n = 0
while a <= b:
    s = a * a + b * b
    if s == c * c:
        print(a)
        n += 1
        a += 1
    elif s < c * c:
        a += 1
    else:
        b -= 1
print(n)
