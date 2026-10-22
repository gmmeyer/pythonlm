s = "abcdef"
out = ""
i = len(s) - 1
while i >= 0:
    out += s[i]
    i -= 1
print(s, "backwards is", out)
print("last letter:", s[-1], "first letter:", s[0])
