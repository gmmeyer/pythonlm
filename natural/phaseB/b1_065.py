n = 210
f = 2
distinct = 0
while f <= n:
    if n % f == 0:
        distinct += 1
        while n % f == 0:
            n //= f
    f += 1
print(distinct)
