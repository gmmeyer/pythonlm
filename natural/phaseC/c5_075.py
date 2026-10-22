word = "stairs"
for i in range(len(word)):
    prefix = ""
    for j in range(i + 1):
        prefix += word[j]
    print(" " * (len(word) - i - 1) + prefix)
