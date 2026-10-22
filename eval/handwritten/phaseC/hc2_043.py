s = "  a tiny  test "
words = 0
best = ""
cur = ""
for i in range(len(s) + 1):
    if i == len(s) or s[i] == " ":
        if len(cur) > 0:
            words += 1
            if len(cur) > len(best):
                best = cur
        cur = ""
    else:
        cur += s[i]
print(words, "words; longest:", best)
