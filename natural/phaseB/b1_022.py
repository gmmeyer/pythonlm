# sum of even Fibonacci numbers below 500
a = 1
b = 2
total = 0
while b < 500:
    if b % 2 == 0:
        total += b
    a, b = b, a + b
print(total)
