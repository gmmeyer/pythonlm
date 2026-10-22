word = "terminal"
out = ""
i = len(word) - 1
while i >= 0:
    out += word[i]
    i -= 1
print(word, "reversed is", out)
