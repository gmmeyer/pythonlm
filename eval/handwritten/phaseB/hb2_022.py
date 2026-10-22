n = 211
k = 0
while n != 495 and k < 8:
    a = n // 100
    b = n // 10 % 10
    c = n % 10
    if a < b:
        a, b = b, a
    if b < c:
        b, c = c, b
    if a < b:
        a, b = b, a
    n = (a - c) * 99
    k += 1
    print(n)
print(k)
