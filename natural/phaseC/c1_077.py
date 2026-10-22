word = "education"
vowels = 0
for i in range(len(word)):
    c = word[i]
    if c == "a" or c == "e" or c == "i" or c == "o" or c == "u":
        vowels += 1
print(f"{word} has {vowels} vowels")
