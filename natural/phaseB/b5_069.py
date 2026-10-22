# greedy: how many squares does it take to build 87 by always taking the biggest?
n = 87
pieces = 0
while n > 0:
    r = 1
    while (r + 1) * (r + 1) <= n:
        r += 1
    n -= r * r
    pieces += 1
    print(r)
print(pieces)
