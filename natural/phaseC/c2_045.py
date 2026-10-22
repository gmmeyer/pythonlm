start = "cold"
goal = "warm"
cur = start
print(cur)
for i in range(len(start)):
    nxt = ""
    for j in range(len(start)):
        if j == i:
            nxt += goal[j]
        else:
            nxt += cur[j]
    cur = nxt
    print(cur)
