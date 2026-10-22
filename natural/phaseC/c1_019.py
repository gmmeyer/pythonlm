word = "pencil"
rev = ""
i = len(word) - 1
while i >= 0:
    rev = rev + word[i]
    i -= 1
print(word, "reversed is", rev)
