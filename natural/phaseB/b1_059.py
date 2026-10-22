# extended Euclid on 46 and 15
a = 46
b = 15
x0, x1 = 1, 0
y0, y1 = 0, 1
while b != 0:
    q = a // b
    a, b = b, a % b
    x0, x1 = x1, x0 - q * x1
    y0, y1 = y1, y0 - q * y1
print(a)
print(x0)
print(y0)
