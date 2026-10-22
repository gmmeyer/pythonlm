s = "never odd or even"
lo = 0
hi = len(s) - 1
ok = True
while lo < hi:
    if s[lo] == " ":
        lo += 1
        continue
    if s[hi] == " ":
        hi -= 1
        continue
    if s[lo] != s[hi]:
        ok = False
        break
    lo += 1
    hi -= 1
print(f"{s}: {ok}")
