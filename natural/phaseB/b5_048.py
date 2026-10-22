a = 5
b = 12
c = 13
valid = a + b > c and a + c > b and b + c > a
print(valid)
print(a * a + b * b == c * c)
if valid:
    print("scalene")
