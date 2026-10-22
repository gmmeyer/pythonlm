s = "aabbbbccdbbbbbe"
best = 0
bc = ""
run = 1
for i in range(1, len(s) + 1):
    if i < len(s) and s[i] == s[i - 1]:
        run += 1
    else:
        if run > best:
            best = run
            bc = s[i - 1]
        run = 1
print(f"longest run: {bc} x {best}")
