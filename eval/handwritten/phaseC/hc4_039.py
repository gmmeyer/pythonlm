# Run-length encoding: each run of a repeated letter becomes the
# letter followed by the length of its run.
s = "aaabccddddeef"
out = ""
run = 1
i = 1
while i <= len(s):
    if i < len(s) and s[i] == s[i - 1]:
        run += 1
    else:
        out = out + s[i - 1] + str(run)
        run = 1
    i += 1
print("input :", s, len(s))
print("output:", out, len(out))
