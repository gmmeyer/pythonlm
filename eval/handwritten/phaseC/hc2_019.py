s = "bookkeeper"
t = s[0]
for i in range(1, len(s)):
    if s[i] != t[-1]:
        t += s[i]
print(t, len(s) - len(t))
