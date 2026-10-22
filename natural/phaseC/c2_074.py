n = 585
s = str(n)
lo = 0
hi = len(s) - 1
same = True
while lo < hi:
    if s[lo] != s[hi]:
        same = False
    lo += 1
    hi -= 1
print(f"{n} reads the same both ways: {same}")
