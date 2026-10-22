text = "learning is fun"
vowels = 0
consonants = 0
for i in range(len(text)):
    c = text[i]
    if c == " ":
        continue
    if c == "a" or c == "e" or c == "i" or c == "o" or c == "u":
        vowels += 1
    else:
        consonants += 1
letters = vowels + consonants
print("vowels:", vowels, "consonants:", consonants)
print("vowel share:", vowels * 100 // letters, "percent")
