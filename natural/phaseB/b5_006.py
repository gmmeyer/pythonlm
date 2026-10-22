# Euclid: count the division steps for gcd(252, 105)
a = 252
b = 105
steps = 0
while b != 0:
    a, b = b, a % b
    steps += 1
print(a)
print(steps)
