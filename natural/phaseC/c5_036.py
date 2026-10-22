word = "stone"
goal = "shine"
for pos in range(len(goal)):
    nxt = ""
    for i in range(len(word)):
        if i == pos:
            nxt += goal[i]
        else:
            nxt += word[i]
    print(" " * pos + word)
    word = nxt
print(" " * len(goal) + word)
