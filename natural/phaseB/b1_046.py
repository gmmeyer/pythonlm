a = 89
b = 55
steps = 0
while b != 0:
    a, b = b, a % b
    steps += 1
print(a)
print(steps)
