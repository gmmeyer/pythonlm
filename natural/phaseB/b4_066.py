a = 3
b = 4
c = 5
if a == b and b == c:
    print("equilateral")
elif a == b or b == c or a == c:
    print("isosceles")
else:
    print("scalene")
if a * a + b * b == c * c:
    print("right angle")
