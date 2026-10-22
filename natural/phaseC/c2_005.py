word = "strength"
pos = -1
i = 0
while i < len(word) and pos == -1:
    c = word[i]
    if c == "a" or c == "e" or c == "i" or c == "o" or c == "u":
        pos = i
    i += 1
if pos == -1:
    print("no vowel in", word)
else:
    print("first vowel in", word, "is", word[pos], "at index", pos)
