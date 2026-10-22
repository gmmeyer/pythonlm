text = "education"
vowels = 0
for i in range(len(text)):
    c = text[i]
    if c == "a" or c == "e" or c == "i" or c == "o" or c == "u":
        vowels += 1
print(text, "has", vowels, "vowels and", len(text) - vowels, "consonants")
