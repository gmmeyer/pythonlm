phrase = "was it a car or a cat i saw"
lo = 0
hi = len(phrase) - 1
ok = True
while lo < hi:
    if phrase[lo] == " ":
        lo += 1
    elif phrase[hi] == " ":
        hi -= 1
    elif phrase[lo] != phrase[hi]:
        ok = False
        break
    else:
        lo += 1
        hi -= 1
print(phrase)
print("palindrome ignoring spaces:", ok)
