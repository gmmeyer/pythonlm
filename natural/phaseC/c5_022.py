s = "aaaaaaabbbbbcc"
out = ""
run = 1
for i in range(1, len(s) + 1):
    if i < len(s) and s[i] == s[i - 1]:
        run += 1
    else:
        out = out + s[i - 1] + str(run)
        run = 1
print(f"{s} ({len(s)}) -> {out} ({len(out)})")
if len(out) < len(s):
    print("saved", len(s) - len(out), "characters")
else:
    print("no gain")
