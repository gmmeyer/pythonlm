s = "WEAREDISCOVERED"
r0 = ""
r1 = ""
r2 = ""
for i in range(len(s)):
    c = i % 4
    if c == 0:
        r0 += s[i]
    elif c == 2:
        r2 += s[i]
    else:
        r1 += s[i]
print(r0 + r1 + r2)
print(r0, r1, r2, sep="|")
