start = "cold"
goal = "warm"
word = start
print(word)
for step in range(4):
    pos = (2 - step) % 4
    nxt = ""
    for i in range(len(word)):
        if i == pos:
            nxt += goal[i]
        else:
            nxt += word[i]
    word = nxt
    print(word)
