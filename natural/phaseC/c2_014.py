s = "aabbbbcdddeee"
best = 1
run = 1
ch = s[0]
for i in range(1, len(s)):
    if s[i] == s[i - 1]:
        run += 1
    else:
        run = 1
    if run > best:
        best = run
        ch = s[i]
print("longest run:", best, "of", ch)
