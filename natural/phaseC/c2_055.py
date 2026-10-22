text = "programming language"
kept = ""
removed = 0
for i in range(len(text)):
    c = text[i]
    if c == "a" or c == "e" or c == "i" or c == "o" or c == "u":
        removed += 1
    else:
        kept += c
print(kept)
print("removed", removed, "vowels")
