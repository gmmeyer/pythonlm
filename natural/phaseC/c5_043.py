# right-align squares in a column of width 4
for n in range(1, 13):
    sq = n * n
    pad = 4 - len(str(sq))
    print(" " * pad + str(sq))
