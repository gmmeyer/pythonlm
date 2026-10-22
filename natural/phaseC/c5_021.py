# run-length encoding, but skip the 1s
s = "wwwwbwwwbb"
out = ""
run = 1
for i in range(1, len(s) + 1):
    if i < len(s) and s[i] == s[i - 1]:
        run += 1
    else:
        out += s[i - 1]
        if run > 1:
            out += str(run)
        run = 1
print(s)
print(out)
