s = "wwwwbbbwwr"
out = ""
i = 0
while i < len(s):
    j = i
    while j < len(s) and s[j] == s[i]:
        j += 1
    out += s[i]
    if j - i > 1:
        out += str(j - i)
    i = j
print(out)
