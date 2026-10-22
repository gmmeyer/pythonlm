s = "abcdefgh"
h = len(s) // 2
out = ""
i = h - 1
while i >= 0:
    out += s[i]
    i -= 1
i = len(s) - 1
while i >= h:
    out += s[i]
    i -= 1
print(out)
print(len(out) == len(s))
