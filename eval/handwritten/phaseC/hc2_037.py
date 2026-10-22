s = "won ton stops"
out = ""
w = ""
for i in range(len(s)):
    if s[i] == " ":
        out += w + " "
        w = ""
    else:
        w = s[i] + w
out += w
print(s)
print(out)
