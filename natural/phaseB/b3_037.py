# row sums of the first five odd-number triangle
n = 1
for row in range(1, 6):
    s = 0
    for k in range(row):
        s += n
        n += 2
    print(s)
