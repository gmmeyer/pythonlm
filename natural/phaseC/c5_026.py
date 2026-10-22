s = "0101010"
ok = True
for i in range(len(s) - 1):
    if s[i] == s[i + 1]:
        ok = False
print(s, "alternates:", ok)
