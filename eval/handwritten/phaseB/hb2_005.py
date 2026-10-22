a = 11
e = 37
m = 29
p = 1
while p <= e // 2:
    p *= 2
r = 1
while p > 0:
    r = r * r % m
    if e // p % 2 == 1:
        r = r * a % m
    p //= 2
print(r)
