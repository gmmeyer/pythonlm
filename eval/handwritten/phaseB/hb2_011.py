h = 0
for n in range(10, 14):
    x = n
    while x != 1 and x != 4:
        s = 0
        while x > 0:
            d = x % 10
            s += d * d
            x //= 10
        x = s
    if x == 1:
        h += 1
        print(n)
print(h)
