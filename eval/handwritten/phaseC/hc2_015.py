s = "an accessibility audit"
out = ""
w = ""
i = 0
while i <= len(s):
    if i == len(s) or s[i] == " ":
        if len(w) > 4:
            w = w[0] + str(len(w) - 2) + w[-1]
        out += w
        if i < len(s):
            out += " "
        w = ""
    else:
        w += s[i]
    i += 1
print(out)
