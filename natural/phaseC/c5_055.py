s = "x9-y2"
for i in range(len(s)):
    c = s[i]
    if "0" <= c <= "9":
        print(c, "is a digit")
    elif "a" <= c <= "z":
        print(c, "is a letter")
    else:
        print(c, "is something else")
