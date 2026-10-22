s = "xyxyxyx"
ok = len(s) >= 2 and s[0] != s[1]
for i in range(2, len(s)):
    if s[i] != s[i - 2]:
        ok = False
print(s, ok)
