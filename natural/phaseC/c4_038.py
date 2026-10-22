print("n  sq")
for n in range(8, 13):
    sq = n * n
    print(n, " " * (4 - len(str(sq))) + str(sq))
