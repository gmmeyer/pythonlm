s = "we are what we do"
out = ""
w = ""
i = len(s) - 1
while i >= -1:
    if i == -1 or s[i] == " ":
        out += w
        if i >= 0:
            out += " "
        w = ""
    else:
        w = s[i] + w
    i -= 1
print(out)
