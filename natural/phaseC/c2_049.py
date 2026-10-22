word = "planet"
distinct = True
for i in range(len(word)):
    for j in range(i + 1, len(word)):
        if word[i] == word[j]:
            distinct = False
print(word, "has all different letters:", distinct)
