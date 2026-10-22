word = "education"
count = 0
for i in range(len(word)):
    c = word[i]
    if c == "a" or c == "e" or c == "i" or c == "o" or c == "u":
        count += 1
print(word, "has", count, "vowels")
