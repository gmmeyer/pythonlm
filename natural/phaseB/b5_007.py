# consecutive Fibonacci numbers are the slowest case for Euclid
a = 987
b = 610
steps = 0
while b > 0:
    r = a % b
    a = b
    b = r
    steps += 1
print(steps)
print(a)
