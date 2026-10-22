s = "abcdefgh"
out = ""
for i in range(0, len(s) - 1, 2):
    out = out + s[i + 1] + s[i]
print(s)
print(out)
