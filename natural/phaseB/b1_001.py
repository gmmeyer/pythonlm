# lcm via gcd
x = 12
y = 18
a = x
b = y
while b > 0:
    t = a % b
    a = b
    b = t
print(a)
print(x * y // a)
