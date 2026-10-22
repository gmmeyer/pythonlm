# are 35 and 64 coprime?
a = 35
b = 64
while b != 0:
    a, b = b, a % b
print(a == 1)
