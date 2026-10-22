word = "bat"
goal = "cog"
print(word, end="")
for pos in range(len(goal)):
    nxt = ""
    for i in range(len(word)):
        if i == pos:
            nxt += goal[i]
        else:
            nxt += word[i]
    word = nxt
    print(" ->", word, end="")
print()
