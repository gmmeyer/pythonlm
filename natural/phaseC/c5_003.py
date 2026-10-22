word = "encyclopedia"
masked = ""
for i in range(len(word)):
    c = word[i]
    if c == "a" or c == "e" or c == "i" or c == "o" or c == "u":
        masked += "*"
    else:
        masked += c
print(word)
print(masked)
