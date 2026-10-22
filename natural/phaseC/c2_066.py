text = "a small step for programmers"
best = 0
cur = 0
for i in range(len(text)):
    if text[i] == " ":
        cur = 0
    else:
        cur += 1
        if cur > best:
            best = cur
print("longest word has", best, "letters")
