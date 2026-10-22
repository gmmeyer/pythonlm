text = "programming is fun"
vowels = 0
i = 0
while i < len(text):
    ch = text[i]
    if ch == "a" or ch == "e" or ch == "i" or ch == "o" or ch == "u":
        vowels += 1
    i += 1
print(f"{text} has {vowels} vowels")
