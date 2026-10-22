# change letters from the right end first
word = "hide"
goal = "hope"
i = len(word) - 1
print(word)
while i >= 0:
    if word[i] != goal[i]:
        new = ""
        for j in range(len(word)):
            if j == i:
                new += goal[j]
            else:
                new += word[j]
        word = new
        print(word)
    i -= 1
