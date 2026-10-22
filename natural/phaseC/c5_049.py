word = "garden"
known = "gaen"
# known holds every letter guessed so far
for i in range(len(word)):
    seen = False
    for j in range(len(known)):
        if known[j] == word[i]:
            seen = True
    if seen:
        print(word[i], end=" ")
    else:
        print("_", end=" ")
print()
