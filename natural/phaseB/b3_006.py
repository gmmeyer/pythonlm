# smallest n whose square is over 200
n = 1
while True:
    sq = n * n
    if sq > 200:
        break
    n += 1
print(n)
print(sq)
