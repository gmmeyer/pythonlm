# sums of 1..n for n = 1..6
for n in range(1, 7):
    s = 0
    for k in range(1, n + 1):
        s += k
    print(s)
