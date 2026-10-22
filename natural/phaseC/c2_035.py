n = 817
s = str(n)
for i in range(len(s)):
    d = s[i]
    if d == "0":
        w = "zero"
    elif d == "1":
        w = "one"
    elif d == "2":
        w = "two"
    elif d == "3":
        w = "three"
    elif d == "4":
        w = "four"
    elif d == "5":
        w = "five"
    elif d == "6":
        w = "six"
    elif d == "7":
        w = "seven"
    elif d == "8":
        w = "eight"
    else:
        w = "nine"
    print(w, end=" ")
print()
