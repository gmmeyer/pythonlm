# differences between consecutive squares
prev = 0
for n in range(1, 11):
    sq = n * n
    print(sq - prev)
    prev = sq
