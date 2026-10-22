# fix a=3 and b=4 and try c from 1 to 8
a = 3
b = 4
for c in range(1, 9):
    if a + b <= c or a + c <= b or b + c <= a:
        print("none")
    elif a * a + b * b == c * c:
        print("right")
    elif a * a + b * b > c * c:
        print("acute")
    else:
        print("obtuse")
