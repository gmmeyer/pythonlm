line = "education is the key"
vowels = 0
for i in range(len(line)):
    c = line[i]
    if c == "a" or c == "e" or c == "i" or c == "o" or c == "u":
        vowels += 1
print(f"{vowels} vowels out of {len(line)} characters")
