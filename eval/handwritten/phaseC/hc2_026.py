s = "coffee"
rep = ""
for i in range(len(s)):
    seen = False
    j = 0
    while j < i:
        if s[j] == s[i]:
            seen = True
            break
        j += 1
    if not seen:
        c = 0
        for j in range(i, len(s)):
            if s[j] == s[i]:
                c += 1
        rep += s[i] + str(c)
print(rep)
