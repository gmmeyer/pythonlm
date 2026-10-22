word = "zigzag"
for i in range(len(word)):
    pos = i % 4
    if pos == 3:
        pos = 1
    print(" " * pos + word[i])
