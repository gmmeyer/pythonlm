s = "xxyyyyzzz"
best = 1
bestch = s[0]
run = 1
for i in range(1, len(s)):
    if s[i] == s[i - 1]:
        run += 1
    else:
        run = 1
    if run > best:
        best = run
        bestch = s[i]
print(f"longest run is {best} x '{bestch}'")
