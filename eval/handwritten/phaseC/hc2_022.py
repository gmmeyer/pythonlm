s = "stack"
out = ""
for i in range(len(s)):
    if i > 0:
        out += "-"
    out += s[i] * (i + 1)
print(out, len(out))
