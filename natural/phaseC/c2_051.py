word = "mississippi"
unique = 0
for i in range(len(word)):
    first = True
    for j in range(i):
        if word[j] == word[i]:
            first = False
    if first:
        unique += 1
print(word, "has", unique, "different letters")
