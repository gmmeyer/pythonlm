s = "aabbbbcdd"
best = 1
run = 1
for i in range(1, len(s)):
    if s[i] == s[i - 1]:
        run += 1
    else:
        run = 1
    if run > best:
        best = run
print("longest run:", best)
