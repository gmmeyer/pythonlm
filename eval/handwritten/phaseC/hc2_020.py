s = "education"
out = ""
hits = 0
i = 0
while i < len(s):
    c = s[i]
    if c == "a" or c == "e" or c == "i" or c == "o" or c == "u":
        out += str(i % 10)
        hits += 1
    else:
        out += c
    i += 1
print(out)
print("vowels:", hits)
