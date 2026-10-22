word = "stressed"
rev = ""
for i in range(len(word)):
    rev = rev + word[len(word) - 1 - i]
print(word, "reversed is", rev)
