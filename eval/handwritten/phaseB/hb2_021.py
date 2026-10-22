n = 840
r = n
m = n
p = 2
while p * p <= m:
    if m % p == 0:
        while m % p == 0:
            m //= p
        r -= r // p
    p += 1
if m > 1:
    r -= r // m
print(r)
