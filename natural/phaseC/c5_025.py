s = "zzzyxxxx"
i = 0
out = ""
while i < len(s):
    j = i
    while j < len(s) and s[j] == s[i]:
        j += 1
    out = out + s[i] + str(j - i)
    i = j
print(s, "=>", out)
