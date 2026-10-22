s = "aaabbcaaaa"
out = ""
run = 1
for i in range(1, len(s)):
    if s[i] == s[i - 1]:
        run += 1
    else:
        out = out + s[i - 1] + str(run)
        run = 1
out = out + s[-1] + str(run)
print(out, len(out))
