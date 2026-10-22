word = "banana"
for i in range(len(word)):
    c = word[i]
    seen = False
    for j in range(i):
        if word[j] == c:
            seen = True
    if not seen:
        n = 0
        for j in range(len(word)):
            if word[j] == c:
                n += 1
        print(c, "->", n)
