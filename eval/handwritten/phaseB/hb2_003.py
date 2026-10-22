n = 987
k = 0
while n > 9:
    s = 0
    while n:
        s += n % 10
        n //= 10
    n = s
    k += 1
print(n)
print(k)
print(n == 1 + (987 - 1) % 9)
