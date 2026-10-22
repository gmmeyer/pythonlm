s = "interpreter"
out = ""
i = 0
while i + 1 < len(s):
    out += s[i + 1] + s[i]
    i += 2
if i < len(s):
    out += s[i]
print(out)
