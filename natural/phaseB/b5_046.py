# classify a triangle from its three sides
a = 7
b = 7
c = 10
if a + b <= c or a + c <= b or b + c <= a:
    print("not a triangle")
elif a == b and b == c:
    print("equilateral")
elif a == b or b == c or a == c:
    print("isosceles")
else:
    print("scalene")
