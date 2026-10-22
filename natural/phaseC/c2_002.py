word = "racecar"
lo = 0
hi = len(word) - 1
ok = True
while lo < hi:
    if word[lo] != word[hi]:
        ok = False
        break
    lo += 1
    hi -= 1
print(word, ok)
