s = "aaabccdddd"
run = 1
for i in range(1, len(s) + 1):
    if i < len(s) and s[i] == s[i - 1]:
        run += 1
    else:
        print(s[i - 1], "x", run)
        run = 1
