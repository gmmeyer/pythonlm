word = "abcdef"
k = 2
out = ""
for i in range(len(word)):
    out += word[(i + k) % len(word)]
print(word, "rotated left by", k, "is", out)
