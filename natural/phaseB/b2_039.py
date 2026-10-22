a = 0
b = 1
steps = 0
while b < 500:
    a, b = b, a + b
    steps += 1
print(a)
print(b)
print(steps)
