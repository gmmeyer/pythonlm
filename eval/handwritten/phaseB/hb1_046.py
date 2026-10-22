a = 3
b = 4
c = 5
for trial in range(4):
    if a + b <= c or a + c <= b or b + c <= a:
        print("not a triangle")
    elif a == b == c:
        print("equilateral")
    elif a == b or b == c or a == c:
        print("isosceles")
    else:
        print("scalene")
    a, b = b, a
    c = c + a - 3
