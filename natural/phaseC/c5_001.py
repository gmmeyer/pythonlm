# vowels vs consonants, written the long way
text = "programming is fun"
vowels = 0
consonants = 0
i = 0
while i < len(text):
    ch = text[i]
    if ch == "a" or ch == "e" or ch == "i" or ch == "o" or ch == "u":
        vowels = vowels + 1
    elif ch != " ":
        consonants = consonants + 1
    i = i + 1
print("vowels:", vowels)
print("consonants:", consonants)
