n = 156
f = 2
largest = 1
while n > 1:
    if n % f == 0:
        largest = f
        n //= f
    else:
        f += 1
print(largest)
