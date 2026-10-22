# Euler's totient of 18
n = 18
count = 0
for k in range(1, n + 1):
    a = k
    b = n
    while b != 0:
        a, b = b, a % b
    if a == 1:
        count += 1
print(count)
