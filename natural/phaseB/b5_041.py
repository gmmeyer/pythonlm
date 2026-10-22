# find a <= b with a*a + b*b == 130
a = 1
b = 12
while a <= b:
    s = a * a + b * b
    if s == 130:
        print(a)
        print(b)
        break
    elif s < 130:
        a += 1
    else:
        b -= 1
