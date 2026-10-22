# lcm of 1..7, built up one number at a time
l = 1
for k in range(2, 8):
    a = l
    b = k
    while b != 0:
        a, b = b, a % b
    l = l * k // a
print(l)
