word = "onomatopoeia"
v = 0
for i in range(len(word)):
    c = word[i]
    if c == "a" or c == "e" or c == "i" or c == "o" or c == "u":
        v += 1
print(f"{v} of {len(word)} letters are vowels ({v * 100 // len(word)}%)")
