a, b = 84, 36
a, b = b, a % b
a, b = b, a % b
print(a)
print(84 // a * 36)
