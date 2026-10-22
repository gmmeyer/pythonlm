n = 907
s = 0
while True:
    if n == 0:
        break
    elif n % 10 == 0:
        n //= 10
        continue
    s += n % 10
    n //= 10
print(s)
print(n)
