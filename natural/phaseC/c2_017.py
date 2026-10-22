word = "stars"
for start in range(len(word)):
    line = ""
    for j in range(start, len(word)):
        line += word[j]
    print(line)
